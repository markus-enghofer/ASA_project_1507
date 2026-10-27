# AgileX

## Data Collection

Data was collected by a manually navigated AgileX LIMO PRO robot. The entire dataset is divided in 20 frames of roughly a few minutes each, covering a large variety of different road surface conditions, height profiles and also anomalies like potholes or troughs. The analysis includes data from an IMU and an 2D LiDAR sensor as well as odometry data, whereby the focus is on linear acceleration and angular velocity measurements which both are provided by an accelerometer and gyroscope integrated in the IMU device. The frames 9, 13, 14, 16 and 20 were recorded by carrying the robot by hand. Hence, these frames are not considered in this analysis. The following list provides a brief description for each of the other frames:

1. **floor:** movement on a flat floor within a building
2. **U-turn:** U-turn on a flat surface within a building
3. **motionless:** No motion inside a building (serves as reference)
4. **zigzagging:** frequent changes of horizontal direction on a flat surface within a building
5. **ramp-down:** movement downwards via a short ramp
6. **footpath:** straight movement on tiles
7. **ramp-up:** movement upwards via a short ramp
8. **rocky-path:** movement slightly downwards on a dirt road with little rocks
10. **plain_road_up:** movement upwards on a tar road in good condition
11. **trough 1:** movement on a tar road with trough (underground speedbreaker)
12. **trough 2:** same as 11 (serves as reference)
15. **off-road:** movement beside the road on uneven and rocky ground
17. **motionless:** No motion on road (serves as reference)
18. **plain_tar_road:** movement on a flat tar-road in rather bad condition
19. **tar_road_pothole:** movement on a section of same tar-road with sequence of potholes

## Preprocessing

Linear acceleration in z-direction (labeled as "az" in dataset) and angular velocity with respect to the x-axis ("gx") turn out to be the best predictor variables to detect road anomalies. As they are heavily impacted by the speed of the robot, both of them are divided by the velocity in x-direction ("vx"). The resulting paramters "az_smooth/vx" and "gx_smooth/vx" thus describe the change of vertical acceleration and pitch per meter driven rather than per second, respectively. Moreover, both parameters were smoothed to reduce noise and make use of the high frequency of the observations. This was done by replacing the respective values of each observation by the weighted mean of the corresponding values of the eleven nearest observations. The weights of each of these observations were calculated based on the index difference with respect to the normal distribution with standard deviation 4. As the timestamps of all observations are equidistant, it was sufficient to just look at the index and not at the time.

## Results

Plots were made to compare the variance of both "az_smooth_vx" and "gx_smooth_vx" across the different frames. As expected, the variance is the larger the worse the subjectively assessed road conditions are. Both parameters hence seem to be good predictors for the quantitative assessment of the road conditions of different road sections. However, single local anomalies like potholes or speedbreakers are hardly recognizable based on the available data as it very noisy. The reason might be the small size of the wheels of the robot as that increases the sensitivity of the sensors also to very small irregularities. Summarizing, the data received by the robot moving by itself reliably assesses the condition of a given road section, but fails to identify particular obstacles. 
