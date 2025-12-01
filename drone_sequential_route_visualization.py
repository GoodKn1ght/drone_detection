import cv2
import matplotlib.pyplot as plt
import numpy as np
from drone_start_point_on_map import find_on_global_map
route_x = []
route_y = []
reverse_route_x = []
reverse_route_y = []
angle, zoom, x, y = find_on_global_map()

absolute_x = 0
absolute_y = 0
current_angle = angle

start_x = x * zoom
start_y = y * zoom
print("\n--- Starting Forward Tracking from Frame 7 to 49 ---\n")
for i in range(7, 49, 1):
    image1 = cv2.imread(f'./crops/crop_{i}.png', cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(f'./crops/crop_{i + 1}.png', cv2.IMREAD_GRAYSCALE)
    if image1 is None or image2 is None:
        continue

    height, width = image1.shape
    template = image1[0:30, width // 2 - 15:width // 2 + 15]

    res = cv2.matchTemplate(image2, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + 30, top_left[1] + 30)

    template_center_x = width // 2
    template_center_y = 15

    matched_center_x = top_left[0] + 15
    matched_center_y = top_left[1] + 15

    offset_x = matched_center_x - template_center_x
    offset_y = matched_center_y - template_center_y

    angle_rad = np.radians(current_angle)

    dx = offset_y * np.cos(angle_rad)
    dy = offset_y * np.sin(angle_rad)

    if i == 7:
        absolute_x = start_x
        absolute_y = start_y
    else:
        absolute_x += dx
        absolute_y -= dy

    route_x.append(absolute_x)
    route_y.append(absolute_y)

    if i > 6:
        frame_angle = np.degrees(np.arctan2(offset_x, offset_y))
        current_angle += ((100*(np.cos(np.deg2rad(current_angle))))/zoom) * frame_angle

    image1_with_rectangle = cv2.cvtColor(image1, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(image1_with_rectangle, (width // 2 - 15, 0), (width // 2 + 15, 30), (0, 255, 0), 2)
    image2_with_rectangle = cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(image2_with_rectangle, top_left, bottom_right, (255, 255, 255), 2)
    arrow_color = (0, 0, 255)
    cv2.arrowedLine(image2_with_rectangle, (width // 2, 15), (top_left[0] + 15, top_left[1] + 15), arrow_color, 3, tipLength=0.05)
    if i < 10:
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.imshow(cv2.cvtColor(image1_with_rectangle, cv2.COLOR_BGR2RGB))
        plt.title(f"Image {i} with Green Square (Original)")
        plt.axis('off')
        plt.subplot(1, 2, 2)
        plt.imshow(cv2.cvtColor(image2_with_rectangle, cv2.COLOR_BGR2RGB))
        plt.title(f"Image {i+1} with White Rectangle and Arrow (Matched Area)")
        plt.axis('off')
        plt.tight_layout()
        plt.draw()
        plt.pause(5)


reverse_absolute_x = start_x
reverse_absolute_y = start_y
reverse_current_angle = 0

print("\n--- Starting Reverse Tracking from Frame 6 to 0 ---\n")

for i in range(6, 0, -1):
    image1 = cv2.imread(f'./crops/crop_{i}.png', cv2.IMREAD_GRAYSCALE)
    image2 = cv2.imread(f'./crops/crop_{i - 1}.png', cv2.IMREAD_GRAYSCALE)
    if image1 is None or image2 is None:
        continue

    height, width = image1.shape
    template = image1[height - 30:height, width // 2 - 15:width // 2 + 15]

    res = cv2.matchTemplate(image2, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    top_left = max_loc
    bottom_right = (top_left[0] + 30, top_left[1] + 30)

    template_center_x = width // 2
    template_center_y = height - 15

    matched_center_x = top_left[0] + 15
    matched_center_y = top_left[1] + 15

    offset_x = matched_center_x - template_center_x
    offset_y = matched_center_y - template_center_y

    angle_rad = np.radians(reverse_current_angle)

    dx = -offset_y * np.cos(angle_rad)
    dy = -offset_y * np.sin(angle_rad)

    reverse_absolute_x -= dx
    reverse_absolute_y -= dy

    reverse_route_x.append(reverse_absolute_x)
    reverse_route_y.append(reverse_absolute_y)

    frame_angle = np.degrees(np.arctan2(offset_x, offset_y)) + 180

    reverse_current_angle -= ((100*(np.cos(np.deg2rad(current_angle))))/zoom) * frame_angle

    image1_with_rectangle = cv2.cvtColor(image1, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(image1_with_rectangle, (width // 2 - 15, height - 30), (width // 2 + 15, height), (0, 255, 0), 2)
    image2_with_rectangle = cv2.cvtColor(image2, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(image2_with_rectangle, top_left, bottom_right, (255, 255, 255), 2)
    arrow_color = (0, 0, 255)
    cv2.arrowedLine(image2_with_rectangle, (width // 2, height - 15), (top_left[0] + 15, top_left[1] + 15), arrow_color, 3, tipLength=0.05)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image1_with_rectangle, cv2.COLOR_BGR2RGB))
    plt.title(f"Image {i} with Green Square (Original)")
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(image2_with_rectangle, cv2.COLOR_BGR2RGB))
    plt.title(f"Image {i-1} with White Rectangle and Arrow (Matched Area)")
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.pause(0.1)

reverse_route_x.reverse()
reverse_route_y.reverse()

full_route_x = reverse_route_x + route_x
full_route_y = reverse_route_y + route_y

angle_differences = []

for i in range(1, len(full_route_x)):
    dx = full_route_x[i] - full_route_x[i - 1]
    dy = full_route_y[i] - full_route_y[i - 1]

    angle_rad = np.arctan2(dy, dx)
    angle_deg = np.degrees(angle_rad)

    angle_differences.append(angle_deg)

print("\n--- Route Coordinates ---")
print("Complete Route X (frames 0-49):", full_route_x)
print("Complete Route Y (frames 0-49):", full_route_y)

plt.figure(figsize=(12, 10))

plt.plot(full_route_x, full_route_y, marker='o', linestyle='-', color='b', label='Full Route (0-49)')

plt.plot(full_route_x[:len(reverse_route_x)], full_route_y[:len(reverse_route_y)],
         marker='x', linestyle='--', color='r', label='Frames 0-6')

plt.plot(full_route_x[len(reverse_route_x):], full_route_y[len(reverse_route_y):],
         marker='+', linestyle='--', color='g', label='Frames 7-49')

plt.plot(full_route_x[0], full_route_y[0], 'ro', markersize=10, label='Frame 0')
if len(full_route_x) > 21:
    plt.plot(full_route_x[21], full_route_y[21], 'co', markersize=10, label='Frame 21')

plt.title('Complete Drone Route (Frames 0-49)')
plt.xlabel('X Position')
plt.ylabel('Y Position')
plt.grid(True)
plt.legend()

print("\n--- Key Coordinates ---")
print("X_0:", full_route_x[0])
print("Y_0:", full_route_y[0])
print("X_21:", full_route_x[21] if len(full_route_x) > 21 else "Not available")
print("Y_21:", full_route_y[21] if len(full_route_y) > 21 else "Not available")

plt.axis('equal')
plt.show()
