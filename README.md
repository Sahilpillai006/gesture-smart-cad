# Gesture Smart CAD

A computer vision hobby project that uses hand gestures to draw, manipulate, and visualize simple 3D-style shapes in real time.

The project uses a webcam to track hand movements and converts those movements into drawing, editing, and object manipulation commands.

---

## Features

- Real-time hand tracking
- Gesture-controlled drawing
- Freehand shape creation
- Shape detection and conversion
- Erase functionality
- Two-hand object manipulation
- Gesture-based scaling
- Gesture-based dragging
- Gesture-based rotation
- 3D-style shape extrusion
- Perspective projection
- Real-time camera interface

---

## How It Works

The system uses the webcam to detect hands using MediaPipe Hands.

The index finger is used as the primary drawing tool. When a drawing path becomes sufficiently long and approximately closed, it is converted into a shape.

Two-hand gestures can then be used to manipulate the most recently created shape.

### Processing Pipeline

    Webcam
       ↓
    OpenCV
       ↓
    MediaPipe Hands
       ↓
    Hand Landmark Detection
       ↓
    Finger Position & Gesture Detection
       ↓
    Drawing / Shape Creation
       ↓
    Shape Manipulation
       ↓
    3D-Style Projection
       ↓
    Real-Time Visual Output

---

## Drawing

With one hand, the index finger can be used to draw a freehand path on the camera interface.

When the path forms a sufficiently closed shape, the system attempts to convert it into a drawable object.

The project can therefore be used to create simple shapes using hand movement instead of a mouse or touchscreen.

---

## Shape Manipulation

The project supports two-hand interaction for manipulating the most recently created shape.

### Scaling

The distance between the two index fingers controls the scale of the selected shape.

Moving the hands farther apart increases the scale, while moving them closer together decreases it.

### Dragging

When both hands perform the required pinch gesture, the object can be moved around the screen.

### Rotation

The angle between the two index fingers is used to rotate the selected shape.

### Two-Hand Controls

    Two Hands
       │
       ├── Distance → Scale
       │
       ├── Position → Drag
       │
       └── Angle → Rotation

---

## 3D-Style Visualization

The project creates a 3D-style representation by taking the drawn 2D shape and generating a second copy at a different depth.

The two layers are connected to visually represent an extruded object.

Perspective projection is then applied to produce a 3D-style appearance on the 2D camera display.

> This is a visual 3D-style projection rather than a complete 3D CAD modelling system.

---

## Gesture Controls

| Gesture / Action | Function |
|---|---|
| Index finger | Draw |
| Index + middle fingers | Erase |
| Two index fingers | Manipulate the latest shape |
| Two-hand pinch | Drag object |
| Hand distance | Scale object |
| Relative hand angle | Rotate object |
| `R` | Clear the drawing |
| `Esc` | Exit the application |

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- Math

---

## Requirements

### Software

- Python 3
- OpenCV
- MediaPipe
- NumPy

### Hardware

- Computer
- Webcam

A working internet connection is required to install the Python dependencies.

---

## Installation

### 1. Clone the repository

    git clone https://github.com/Sahilpillai006/gesture-smart-cad.git

### 2. Move into the project directory

    cd gesture-smart-cad

### 3. Install the required libraries

    pip install -r requirements.txt

---

## Usage

Run the program:

    python main.py

Allow the application to access your webcam.

Use your index finger to draw on the camera interface.

Create a shape and use the supported two-hand gestures to manipulate it.

Press `R` to clear the drawing.

Press `Esc` to exit the application.

---

## Limitations

This project is an experimental hobby project and has some limitations:

- The system depends on webcam quality and lighting conditions.
- Hand tracking may become unstable with fast movements or occlusion.
- Shape creation depends on the drawn path being sufficiently closed.
- Only the latest created shape is manipulated.
- The 3D representation is a visual extrusion and projection rather than a full 3D model.
- The system does not provide professional CAD features such as precise measurements, constraints, or parametric modelling.
- Gesture detection is based on hand landmark positions and simple geometric calculations.

---

## Future Upgrades

Possible improvements include:

- Improve gesture recognition reliability.
- Add multiple selectable objects.
- Add object deletion and duplication.
- Add precise shape primitives such as cubes, cylinders, and spheres.
- Improve 3D transformation controls.
- Add depth-aware interaction.
- Add object selection.
- Add undo and redo functionality.
- Add keyboard shortcuts for additional operations.
- Export created objects to standard 3D formats.
- Add a proper 3D rendering engine.
- Add more advanced CAD operations.

---

## Project Background

This project was created as a personal hobby experiment to explore computer vision, hand tracking, gesture-based interaction, and 3D-style visualization.

The main idea was to investigate whether hand movements could be used as an alternative interface for drawing and manipulating digital objects.

---

## Project Status

**Status: Completed Hobby Experiment**

This project was originally developed as a personal hobby project.

The repository preserves the original concept while providing documentation and a cleaner structure for future development.

---

## Author

**Sahil B Pillai**

Engineer | Robotics & AI Enthusiast

---

## License

This project is open source and available under the MIT License.