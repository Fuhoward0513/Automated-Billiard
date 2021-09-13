# Automated Billiard Project
![](https://i.imgur.com/vIP16V4.png)

## :star: Project Description
### Automated Billiard Ball Machine Implemented with Manipulator and 3D Computer-Vision in High Accuracy:
Create a system combined with manipulator and depth-camera to play billiard ball automatically. The system includes Image-processing (Mask, Opening, Hough Circle Transformation) and AI (Simple Object Detection with Tensorflow) to apply object detection, Robot-Vision (Camera Calibration, Hand-Eye Calibration),Algorithm designed by ourselves to find the optimal solution to win the game, and Manipulator Kinematics to apply coordinate transformation.

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
Get the extrinstic matrix between the end-effector and the camera
#### 4. Get intristic camera matrix with OpenCV
Get the intrinstic matrix and the distortion factor

![](https://i.imgur.com/Ao856mV.png)

### Ball Detection and Algorithm
#### 1. 1. Take color image (color.png) and depth image (config/depth.npy)
```
align_depth2color.take_pic()
```
![](https://i.imgur.com/wzxLL4S.png)

> :bulb: Note: the left is RGB image, the right is depth image

#### 2. Undistort the color image and the depth image
```
test_undistort.undistort()
```
![](https://i.imgur.com/53jNJMv.jpg)

> :bulb: Note: the obvious black lines around the picture are the consequence of the correction of distortion

#### 3. Image noise reduction with applying Mask and Opening(morphology)
a. Apply green mask to the color image(bitwise_and)

![](https://i.imgur.com/9Cuwfs7.jpg)

b. Detect the edge of the table, using the picture above

![](https://i.imgur.com/5rogd6i.png)

c. Apply opening to reduce the image noise and save the image(mask.png)
![](https://i.imgur.com/Q6XhKqb.png)


#### 4. Find the Holes of the table (config/hole.txt)
Applying Hough Circle Transformation to find the coordinates of the table holes from the mask.png
Find Holes coordinates of the table with Hough Circle Transformation
```
findHole_new.findHole()
```
![](https://i.imgur.com/8DHfp1q.png)

#### 5. Simple Object Detection with Tensorflow to classify balls as Cue ball and others

![](https://i.imgur.com/EydDtA3.jpg)


#### 6. Find Balls coordinates(config/white_pixel.txt, config/ball_pixel.txt)
```
hough_circle_test.findBall()
```
a. Apply bitwise_and between the color image and mask.png 

![](https://i.imgur.com/dTtfHfi.png)

b. Apply Hough Circle Transformation to find the balls' coordinates

![](https://i.imgur.com/NgupYDi.jpg)


#### 7. Apply Billiard Ball Strategy Algorithm to find optimal solution
```
num_ball, isConvex = hit_ball_strategy.hit_ball_strategy()
```
The best solution to the case will be visualize on the image.
> :bulb: Note: To see the rules of the strategy, you can turn to the Readme in the "algorithm/"
> 

![](https://i.imgur.com/CBxhUng.jpg)

#### 8. Coordinate Transformation from Image Coordinate to Robot Base Coordinate(World Coordinate) and Hit the Ball !
The coordinate of the cue ball(image coordinate) will be transformed into Robot-Base coordinate, and the manipulator will hit the ball with the Pneumatic cylinder.
```
coordinate_transformation.coordinate_transformation(num_ball, isConvex)
```
![](https://i.imgur.com/iruHybB.png)



## :mag_right: Demonstration

### To see the details of our program and the demonstration video, you can click the web address blow !

:point_right: Our Yutube Channel:  https://youtu.be/1msCYlrSwBo


