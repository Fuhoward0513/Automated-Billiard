# Automated Billiard Project
## :star: Project Description
### Automated Billiard Ball Machine Implemented with Manipulator and 3D Computer-Vision in High Accuracy:
Create a system combined with manipulator and depth-camera to play billiard ball automatically. The system includes Image-processing (Mask, Opening, Hough Circle Transformation) and AI (Simple Object Detection with Tensorflow) to apply object detection, Robot-Vision (Camera Calibration, Hand-Eye Calibration), and Manipulator Kinematics to apply coordinate transformation.

> :bulb: Note: To see the final demonstration without reading the description, you can goto our Youtube watching the demonstration video!
> 
> :point_right:  https://youtu.be/1msCYlrSwBo

## :orange_book:  Test execution

### Eye-Hand Calibration and Camera Calibration with “ChAruco Board”
#### 1. Execute camera_eye_hand.py
```
python /eye_hand/camera_eye_hand.py
```

### Ball Detection and Algorithm
#### 1. Execute main.py
```
python main.py
```
#### 2. After seeing the prompt text "Continue: press c", press "c" to start the execute the program
#### 3. The Manipulator will hit the ball automatically
#### 4. Repeat the process by pressing "c" again; Stop the process by pressing the word except "c"

## :earth_africa: Program Flow
### Eye-Hand Calibration and Camera Calibration with “ChAruco Board”
#### 1. Open the HIWIN_Contest UI
Connect to the manipulator and turn on the "SMON"

![](https://i.imgur.com/7O9CLiL.png)

#### 2. Execute camera_eye_hand.py
Pose controlling Robot Manipulator to take pictures of “ChAruco Board” 

![](https://i.imgur.com/t8YxIbG.png)

![](https://i.imgur.com/b0GYvXi.png)

![](https://i.imgur.com/eL36ibr.png)

#### 3. Pose estimation to “ChAruco Board” and apply hand-eye calibration with OpenCV
#### 4. Get intristic camera matrix with OpenCV

![](https://i.imgur.com/Ao856mV.png)

## Ball Detection and Algorithm






