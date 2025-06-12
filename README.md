# Virtual Try-On Stable Application

A real-time virtual clothing try-on application that uses advanced computer vision to overlay shirts naturally on users through their webcam feed. The application leverages MediaPipe for precise pose detection and implements sophisticated smoothing algorithms for stable, realistic clothing overlay.

## Key Capabilities

### Real-Time Pose Detection & Tracking
- **MediaPipe Integration**: Uses MediaPipe Pose with optimized settings for real-time performance  
- **Landmark-Based Fitting**: Tracks shoulder (landmarks 11, 12) and hip (landmarks 23, 24) positions for accurate torso measurement
- **Dynamic Sizing**: Automatically calculates torso dimensions and scales clothing accordingly 

### Advanced Stabilization System
- **Exponential Smoothing**: Implements smoothing with alpha=0.8 to reduce jitter and provide natural movement
- **Angle Stabilization**: Clips rotation to ±30 degrees and ignores extreme angles >60 degrees for realistic appearance 
- **Position Smoothing**: Smooths position, size, and rotation parameters to prevent flickering 

### Professional Image Processing
- **Alpha Channel Support**: Full BGRA transparency support for natural clothing overlay  
- **Geometric Transformations**: Applies rotation and scaling with proper interpolation
- **Boundary Handling**: Intelligent clipping to prevent overlay artifacts at frame edges

### Interactive Controls
- **Multi-Shirt Support**: Load and switch between multiple PNG shirt assets
- **Real-Time Switching**: Navigate through shirts with 'N' (next) and 'P' (previous) keys 
- **Visual Feedback**: On-screen display showing current shirt selection

## System Requirements

- **Python**: 3.8 or higher
- **Hardware**: Webcam (USB or built-in)
- **OS**: Windows, macOS, or Linux
- **Dependencies**: OpenCV, MediaPipe, NumPy (see requirements.txt)

## Installation & Setup

### 1. Repository Setup
```bash
git clone https://github.com/Natykibur/Virtual_TRYON_STABLE.git
cd Virtual_TRYON_STABLE
```

### 2. Environment Setup
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Asset Preparation
- Create an `assets` directory in the project root
- Add PNG shirt images with transparent backgrounds to the `assets` folder
- Ensure images have proper alpha channels for transparency
- Recommended image size: 500x600 pixels or similar aspect ratio

### 4. Launch Application
```bash
python virtual_tryon_stable/main.py
```

## Usage Instructions

### Controls
- **'N' Key**: Switch to next shirt
- **'P' Key**: Switch to previous shirt  
- **'ESC' Key**: Exit application

### Optimal Usage Tips
- **Lighting**: Use well-lit environment for better pose detection
- **Background**: Plain background improves tracking accuracy
- **Positioning**: Stand 3-6 feet from camera with full torso visible
- **Movement**: Smooth, natural movements work best with the stabilization system

## Technical Architecture

The application follows a modular real-time processing pipeline:

1. **Frame Capture**: Continuous webcam input via OpenCV
2. **Pose Analysis**: MediaPipe processes RGB frames for landmark detection
3. **Geometry Calculation**: Computes torso dimensions and orientation
4. **Stabilization**: Applies smoothing filters to reduce jitter
5. **Image Transformation**: Scales, rotates, and positions shirt overlay
6. **Alpha Compositing**: Blends shirt with background using transparency
7. **Display Rendering**: Outputs final composite frame

## Project Structure

```
Virtual_TRYON_STABLE/
├── virtual_tryon_stable/
│   └── main.py              # Core application logic
├── assets/                  # Shirt PNG files (user-provided)
├── requirements.txt         # Python dependencies
└── README.md               # Documentation
```

## Troubleshooting

- **No shirts detected**: Ensure PNG files are in the `assets` directory
- **Poor tracking**: Check lighting and camera positioning
- **Performance issues**: Reduce camera resolution or close other applications
- **Import errors**: Verify all dependencies are installed correctly

---

