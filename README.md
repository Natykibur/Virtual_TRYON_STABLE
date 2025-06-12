# Virtual Try-On Application

A real-time virtual try-on application that allows users to try different shirts using their webcam. The application uses MediaPipe for pose detection and OpenCV for image processing.

## Features

- Real-time shirt overlay on webcam feed
- Multiple shirt options with easy switching
- Smooth tracking and natural movement
- Keyboard controls for shirt selection

## Requirements

- Python 3.8 or higher
- Webcam
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/virtual-tryon.git
cd virtual-tryon
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Place your shirt images (PNG format with transparency) in the `assets` directory
2. Run the application:
```bash
python main.py
```

3. Controls:
- Press 'N' to switch to the next shirt
- Press 'P' to switch to the previous shirt
- Press 'ESC' to exit

## Project Structure

```
virtual-tryon/
├── assets/           # Directory for shirt images
├── main.py          # Main application code
├── requirements.txt # Python dependencies
└── README.md       # Project documentation
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
