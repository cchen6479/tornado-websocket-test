import cv2
from colors import colors

def detect_balls(frame, color):
    output_image = frame
    if not(color == "none"):
        color_bounds = tuple(colors[color].values())
        low = color_bounds[:3]
        upper = color_bounds[3:]

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, low, upper)
        if color == "red":
            mask = cv2.bitwise_not(mask)
        output_image = cv2.bitwise_and(frame, frame, mask = mask)

    output_image = cv2.flip(output_image, 1)
    cv2.imwrite("frame.jpg", output_image)