import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import datetime

patch = "F:\\Studyspace\\DoAn\\CountFish\\demcaaa\\12.mp4"

cap = cv2.VideoCapture(patch)


if not cap.isOpened():
    print("Cannot open camera")
    exit()


DURATION = 10

EDGE_TOP = 50
EDGE_RIGHT = 500
EDGE_BOTTOM = 350
EDGE_LEFT = 100

TIME_DURATION = datetime.datetime.now() + datetime.timedelta(seconds=DURATION)
# time_duration = datetime.datetime.now()+datetime.timedelta(minutes=DURATION)


while True:

    _, img = cap.read()

    img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img_cvtc = img_cvt.copy()
    cv2.rectangle(img_cvtc, (EDGE_LEFT, EDGE_TOP),
                  (EDGE_RIGHT, EDGE_BOTTOM), (0, 0, 255), 5)

    ROI = img_cvt[EDGE_TOP:EDGE_BOTTOM, EDGE_LEFT:EDGE_RIGHT]

    gray = cv2.cvtColor(ROI, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (15, 15), 0)

    ret, threshold = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(
        threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnt_info = []

    fish_contour = np.zeros(threshold.shape)
    count = 0
    for cnt in contours:

        area = round(cv2.contourArea(cnt))

        if area > 50 and 0 not in cnt:

            if 0 or threshold.shape[1] - 1 not in (cnt[i][0][0] for i in range(len(cnt))):

                if 0 or threshold.shape[0] - 1 not in (cnt[i][0][1] for i in range(len(cnt))):

                    cv2.drawContours(fish_contour, [cnt], 0, 255, -1)

                    count = count + 1

    cv2.imshow("Edge", img_cvtc)
    cv2.imshow("Thresh", fish_contour)

    year, month, day = time.strftime(
        '%Y'), time.strftime('%m'), time.strftime('%d')

    now = datetime.datetime.now().strftime("%H:%M:%S.%f")
    # timing = time.strftime('%H:%M:%S:%F')

    print("Time {}-{}/{}/{}".format(now, day, month, year))
    print("count: ", str(count))

    time.sleep(0.1)

    if datetime.datetime.now() > TIME_DURATION:
        break
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
