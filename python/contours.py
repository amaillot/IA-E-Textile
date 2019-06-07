import cv2
import numpy as np

cam = cv2.VideoCapture(0)
while True:
    _, frame = cam.read()
    print("frame : ")
    print(frame)
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([38, 86, 0])
    upper_blue = np.array([121, 255, 255])

    sensitivity = 15
    lower_white = np.array([0, 0, 255 - sensitivity])
    upper_white = np.array([255, sensitivity, 255])

    # lower_white = np.array([0, 0, 0], dtype=np.uint8)
    # upper_white = np.array([0, 0, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_white, upper_white)

    res = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for contour in contours:
        cv2.drawContours(frame, contour, -1, (0, 255, 0), 3)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    # cv2.imshow("Res", res)
    key = cv2.waitKey(1)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()