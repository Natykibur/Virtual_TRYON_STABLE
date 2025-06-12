import cv2
import numpy as np
import mediapipe as mp
import os
import glob

def load_shirts(directory):
    shirts = []
    # Look for PNG files in the assets directory
    for path in glob.glob(os.path.join(directory, "*.png")):
        shirt = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if shirt is not None:
            shirts.append(shirt)
    if not shirts:
        raise FileNotFoundError(f"No shirt images found in: {directory}")
    return shirts

def overlay_transparent(bg, overlay, x, y):
    if overlay.shape[2] < 4:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_BGR2BGRA)

    h, w = overlay.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    if x < 0: overlay = overlay[:, -x:]; w += x; x = 0
    if y < 0: overlay = overlay[-y:, :]; h += y; y = 0
    if x + w > bg_w: overlay = overlay[:, :bg_w - x]; w = bg_w - x
    if y + h > bg_h: overlay = overlay[:bg_h - y, :]; h = bg_h - y

    if h <= 0 or w <= 0:
        return bg

    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        bg[y:y+h, x:x+w, c] = (
            alpha * overlay[:, :, c] + (1 - alpha) * bg[y:y+h, x:x+w, c]
        )
    return bg

def get_point(lm, i, w, h):
    return int(lm[i].x * w), int(lm[i].y * h)

def smooth(prev, curr, factor):
    return int(prev * factor + curr * (1 - factor))

# Initialize shirt collection
SHIRTS_DIR = "assets"
shirts = load_shirts(SHIRTS_DIR)
current_shirt_index = 0
shirt_img = shirts[current_shirt_index]

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
cap = cv2.VideoCapture(0)

# Get camera dimensions
ret, frame = cap.read()
if ret:
    frame_height, frame_width = frame.shape[:2]
    # Reset the video capture
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
else:
    frame_width, frame_height = 640, 480  # Default dimensions

px, py, pw, ph, pa = 0, 0, 0, 0, 0
alpha = 0.8

print("Controls:")
print("N - Next shirt")
print("P - Previous shirt")
print("ESC - Exit")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    if result.pose_landmarks:
        lm = result.pose_landmarks.landmark
        l_sh, r_sh = get_point(lm, 11, w, h), get_point(lm, 12, w, h)
        l_hip, r_hip = get_point(lm, 23, w, h), get_point(lm, 24, w, h)

        mid_sh = ((l_sh[0] + r_sh[0]) // 2, (l_sh[1] + r_sh[1]) // 2)
        mid_hip = ((l_hip[0] + r_hip[0]) // 2, (l_hip[1] + r_hip[1]) // 2)

        torso_height = np.linalg.norm(np.subtract(mid_sh, mid_hip))
        torso_width = np.linalg.norm(np.subtract(l_sh, r_sh))

        raw_angle = np.degrees(np.arctan2(r_sh[1] - l_sh[1], r_sh[0] - l_sh[0]))
        if abs(raw_angle) > 60:
            angle = pa
        else:
            angle = np.clip(raw_angle, -30, 30)

        # Adjusted scaling factors for better width
        target_w = int(torso_width * 1.3)  # Increased width scaling
        target_h = int(torso_height * 1.5)
        center_x, center_y = mid_sh

        px = smooth(px, center_x, alpha)
        py = smooth(py, center_y - int(torso_height * 0.1), alpha)
        pw = smooth(pw, target_w, alpha)
        ph = smooth(ph, target_h, alpha)
        pa = smooth(pa, angle, alpha)

        resized = cv2.resize(shirt_img, (pw, ph), interpolation=cv2.INTER_AREA)
        M = cv2.getRotationMatrix2D((pw // 2, ph // 4), pa, 1)
        rotated = cv2.warpAffine(resized, M, (pw, ph), borderValue=(0, 0, 0, 0))

        frame = overlay_transparent(frame, rotated, px - pw // 2, py - ph // 4)

    # Add text showing current shirt number
    cv2.putText(frame, f"Shirt {current_shirt_index + 1}/{len(shirts)}", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Stable Try-On", frame)
    key = cv2.waitKey(1) & 0xFF
    
    if key == 27:  # ESC
        break
    elif key == ord('n'):  # Next shirt
        current_shirt_index = (current_shirt_index + 1) % len(shirts)
        shirt_img = shirts[current_shirt_index]
    elif key == ord('p'):  # Previous shirt
        current_shirt_index = (current_shirt_index - 1) % len(shirts)
        shirt_img = shirts[current_shirt_index]

cap.release()
cv2.destroyAllWindows()
