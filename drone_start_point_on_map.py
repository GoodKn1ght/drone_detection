import cv2
import numpy as np

image_path = "global_map.png"
template_files = ["./crops/crop_7.png"]

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, -angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def scale_image(image, percent, maxwh):
    max_width = maxwh[1]
    max_height = maxwh[0]
    max_percent_width = max_width / image.shape[1] * 100
    max_percent_height = max_height / image.shape[0] * 100
    max_percent = 0
    if max_percent_width < max_percent_height:
        max_percent = max_percent_width
    else:
        max_percent = max_percent_height
    if percent > max_percent:
        percent = max_percent
    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    result = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return result, percent

def find_on_global_map():
    image = cv2.imread(image_path)
    image = cv2.resize(image, (image.shape[1] // 3, image.shape[0] // 3))
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    best_match = None
    best_zoom = 0
    best_angle = 0
    x_center = 0
    y_center = 0

    for template_file in template_files:
        template = cv2.imread(template_file, cv2.IMREAD_GRAYSCALE)

        max_val = 0
        best_match = None
        best_zoom = 0
        best_angle = 0
        best_rotated_template = None

        for zoom in np.arange(3, 12, 0.1):
            percent = 100 / zoom
            resized_template, actual_percent = scale_image(template, percent, (image.shape[0], image.shape[1]))

            for angle in range(0, 360, 10):
                rotated_image = rotate_image(resized_template, angle)
                result = cv2.matchTemplate(image_gray, rotated_image, cv2.TM_CCOEFF_NORMED)
                min_val, max_val_candidate, min_loc, max_loc = cv2.minMaxLoc(result)

                if max_val_candidate > max_val:
                    max_val = max_val_candidate
                    best_match = max_loc
                    best_zoom = zoom
                    best_angle = angle
                    best_rotated_template = rotated_image

        x_center = best_match[0] + best_rotated_template.shape[1] // 2
        y_center = best_match[1] + best_rotated_template.shape[0] // 2

    return best_angle, best_zoom, x_center, y_center

def main():
    angle, zoom, x, y = find_on_global_map()
    print("--- Match Results ---")
    print(f"Angle: {angle} degrees")
    print(f"Zoom: {zoom}")
    print(f"X: {x}, Y: {y}")

if __name__ == "__main__":
    main()
