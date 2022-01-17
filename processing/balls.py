import cv2
from processing.constants import colors, width, height
import numpy as np


# parameters: image frame and color of mask from websocket message
def detect_balls(frame, color):
    output_image = frame
    if not(color == "none"):

        # declare color bounds
        color_bounds = tuple(colors[color].values())
        low = color_bounds[:3]
        upper = color_bounds[3:]

        # creates mask
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, low, upper)
        masked_image = cv2.bitwise_and(frame, frame, mask = mask)

        # prepares for circle detection
        gray_masked_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
        eroded_masked_image = cv2.erode(gray_masked_image, None, iterations = 2)
        circles = cv2.HoughCircles(eroded_masked_image, cv2.HOUGH_GRADIENT, 1, 101, param1 = 118, param2 = 18, minRadius=0, maxRadius=0)

        # draws bounding boxes and writes coordinates
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                cv2.rectangle(frame, (i[0] - i[2], i[1] - i[2]), (i[0] + i[2], i[1] + i[2]), (0, 255, 0), 2)
                cv2.putText(frame, f"({i[0] - width/2}, {-1 * i[1] + height / 2})", (i[0] - i[2], i[1] - i[2]), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0))

        output_image = frame

    return output_image