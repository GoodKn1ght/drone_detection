import cv2
import numpy as np
import matplotlib.pyplot as plt
from drone_sequential_route import track_drone_route

route_x, route_y, zoom = track_drone_route()

global_map = cv2.imread('global_map.png')

if global_map is None:
    print("Error: Could not load the map image.")
    exit()

global_map = cv2.resize(global_map, (global_map.shape[1] // 3, global_map.shape[0] // 3))

map_with_path = global_map.copy()

scaled_route_x = [x / zoom for x in route_x]
scaled_route_y = [y / zoom for y in route_y]

scaled_route_x = np.clip(scaled_route_x, 0, global_map.shape[1] - 1)
scaled_route_y = np.clip(scaled_route_y, 0, global_map.shape[0] - 1)

for i in range(1, len(scaled_route_x)):
    start_point = (int(scaled_route_x[i - 1]), int(scaled_route_y[i - 1]))
    end_point = (int(scaled_route_x[i]), int(scaled_route_y[i]))
    cv2.line(map_with_path, start_point, end_point, (255, 0, 0), 2)

for i in range(len(scaled_route_x)):
    point = (int(scaled_route_x[i]), int(scaled_route_y[i]))
    cv2.circle(map_with_path, point, 5, (0, 0, 255), -1)

plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(map_with_path, cv2.COLOR_BGR2RGB))
plt.title("Drone's Path on Global Map")
plt.axis('off')
plt.show()
