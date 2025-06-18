# Drone Sequential Route Visualization

This project visualizes the trajectory formed between sequential images captured by a drone.  
It uses OpenCV's `matchTemplate` function to track and visualize the path of the drone.

## Description

The `drone_sequential_route_visualization` file helps you visualize how the trajectory 
is created between each sequential image.  
This file is independent, and you can easily run it to see 50 plots.

Additionally, the `matchTemplate` function from OpenCV is used for this purpose.  
The technique was also used in the `drone_start_point_on_map` file, but in that case,
brute force is employed to find the correct scale and angle for the provided image.  
This is necessary because the classic approach doesn’t work on a global map.

## File Breakdown

- **`drone_sequential_route_visualization`**:  
  Visualizes the sequential trajectory between images.

- **`drone_start_point_on_map`**:  
  Applies brute force to find the correct scale and angle for the global map.

- **`crop_7.png`**:  
  A chosen image that contains vital features for easy identification, 
- with a zoom of 11.7 and an angle of 60.

## Process

1. **Sequential Scan**:  
   A forward and backward sequential scan is applied to recreate the full road on the global map.

2. **Angle Tracking**:  
   The angle is tracked to find the correct `dx` and `dy` values on the global map, which differ 
   from the crops.  
   These changes are logged in the console for easier tracking.

3. **Visualization**:  
   50 plots are visualized to demonstrate the movement and trajectory between the images.

## How to Use

1. Run the `drone_sequential_route_visualization` to visualize 50 plots of the drone's trajectory.

2. To view the final result, start `drone_whole_road_on_map`.

