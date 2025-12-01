import cv2
import numpy as np
from drone_start_point_on_map import find_on_global_map

def track_drone_route():
    angle, zoom, x, y = find_on_global_map()

    route_x = []
    route_y = []
    reverse_route_x = []
    reverse_route_y = []

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
            print(f"Failed to load image {i} or {i + 1}. Skipping...")
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

        print(f"Frame {i}: offset_x={offset_x}, offset_y={offset_y}, current_angle={current_angle}")
        print(f"Calculated: dx={dx}, dy={dy}")

        if i == 7:
            absolute_x = start_x
            absolute_y = start_y
        else:
            absolute_x += dx
            absolute_y -= dy

        route_x.append(absolute_x)
        route_y.append(absolute_y)

        print(f"Updated position: absolute_x={absolute_x}, absolute_y={absolute_y}")

        if i > 6:
            frame_angle = np.degrees(np.arctan2(offset_x, offset_y))
            current_angle += ((100*(np.cos(np.deg2rad(current_angle))))/zoom) * frame_angle

            print(f"Frame angle: {frame_angle:.2f} degrees")

    reverse_absolute_x = start_x
    reverse_absolute_y = start_y
    reverse_current_angle = 0

    print("\n--- Starting Reverse Tracking from Frame 6 to 0 ---\n")

    for i in range(6, 0, -1):
        print(f"\nProcessing frame {i} to {i - 1}...")

        image1 = cv2.imread(f'./crops/crop_{i}.png', cv2.IMREAD_GRAYSCALE)
        image2 = cv2.imread(f'./crops/crop_{i - 1}.png', cv2.IMREAD_GRAYSCALE)
        if image1 is None or image2 is None:
            print(f"Failed to load image {i} or {i - 1}. Skipping...")
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

        print(f"Reverse Frame {i}: offset_x={offset_x}, offset_y={offset_y}, current_angle={reverse_current_angle}")
        print(f"Calculated: dx={dx}, dy={dy}")

        reverse_absolute_x -= dx
        reverse_absolute_y -= dy

        reverse_route_x.append(reverse_absolute_x)
        reverse_route_y.append(reverse_absolute_y)

        print(f"Updated position: absolute_x={reverse_absolute_x}, absolute_y={reverse_absolute_y}")

        frame_angle = np.degrees(np.arctan2(offset_x, offset_y)) + 180
        reverse_current_angle -= ((100*(np.cos(np.deg2rad(current_angle))))/zoom) * frame_angle

        print(f"Frame angle: {frame_angle:.2f} degrees")

    reverse_route_x.reverse()
    reverse_route_y.reverse()

    full_route_x = reverse_route_x + route_x
    full_route_y = reverse_route_y + route_y

    return full_route_x, full_route_y, zoom
