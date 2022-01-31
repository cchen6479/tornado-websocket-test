import cv2
from processing.constants import camera
import math

cap = cv2.VideoCapture(camera, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_EXPOSURE, -7)

MIN_AREA = 1000

# cv2.namedWindow("canny-ing")
# def findline(val):
#     pass

# cv2.createTrackbar("low thresh", "canny-ing", 50, 100, findline)
# cv2.createTrackbar("high thresh", "canny-ing", 50, 100, findline)

# def canny_edge(frame):
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     canny = cv2.Canny(blur, cv2.getTrackbarPos("low thresh", "canny-ing"), cv2.getTrackbarPos("high thresh", "canny-ing"))
#     _, mask = cv2.threshold(canny, 70, 255, cv2.THRESH_BINARY)
#     return mask

def sobel_edge(frame):
    ddepth = cv2.CV_16S
    scale = 1
    delta = 0

    frame = cv2.GaussianBlur(frame, (3, 3), 0)
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    grad_x = cv2.Sobel(gray, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv2.BORDER_DEFAULT)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return grad

def laplace_edge(frame):
    ddepth = cv2.CV_16S
    kernel_size = 3

    src = cv2.GaussianBlur(frame, (3, 3), 0)

    src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
   
    dst = cv2.Laplacian(src_gray, ddepth, ksize=kernel_size)

    abs_dst = cv2.convertScaleAbs(dst)
    return abs_dst

def isRect(cnt, approx, ar):
    return len(approx) == 4 and cv2.contourArea(cnt) > MIN_AREA and not (0.8 <= ar <= 1.2)

#bgr mask and to gray
def maskColor(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mask = cv2.inRange(frame, (0, 0, 0), (50, 50, 50))
    frame = cv2.bitwise_and(frame, frame, mask = mask)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return frame

def findRect(frame, output):
    contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for(index, contour) in enumerate(contours):
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * peri, True)
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = w/h

        if isRect(contour, approx, aspect_ratio):

            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0))

            _,cols = frame.shape[:2]
            [vx,vy,x,y] = cv2.fitLine(contour, cv2.DIST_L2,0,0.01,0.01)
            lefty = int((-x*vy/vx) + y)
            righty = int(((cols-x)*vy/vx)+y)
            p1 = (cols-1,righty)
            p2 = (0, lefty)
            cv2.line(output,p1,p2,(0,0,255),2)
            print(get_angle(p1, p2))
            cv2.putText(output, f"{str(get_angle(p1, p2))} degrees", (int(x), int(y-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255,255)  )

def get_angle(p1, p2):
    m = (p1[1] - p2[1])/(p1[0] - p2[0])
    return format(math.atan(m) * -180 / math.pi, '.2f')    

def detect_line(frame):
    masked_frame = maskColor(frame)

    findRect(masked_frame, frame)
    
    return frame

if __name__ == "__main__":
    while True:
        _, frame = cap.read()
        output = detect_line(frame)
        cv2.imshow("fraem", output)
        if cv2.waitKey(1) == ord('q'):
            break