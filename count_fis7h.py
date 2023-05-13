import cv2
import numpy as np
# import matplotlib.pyplot as plt
import time
import datetime

import paho.mqtt.client as paho
from paho import mqtt


from pymongo import MongoClient

from constant import BROKER_URL, BROKER_PORT, BROKER_USERNAME, BROKER_PASSWORD,MONGODB_URL, PATH_SAVE_INFO_FEEDER
import random
import json
from bson.objectid import ObjectId


# patch = "/home/doan/Desktop/DA/WebServer/Aquarium-Smart/my_data/12.mp4"

# db_client=MongoClient()

# db_client = MongoClient(MONGODB_URL)
# mydatabase = db_client["test"]
# collection_name = mydatabase["amount_fish"]
# collection_food = mydatabase["food"]


# read json

# with open(PATH_SAVE_INFO_FEEDER, 'r') as open_file:
#   data_feeder = json.load(open_file)
#   print("data_feeder: ", data_feeder)
#   collection_food.update_one({"_id" : ObjectId(str(data_feeder["id"])) }, {"$set": {"status": "COMPLETE"}})




# cap = cv2.VideoCapture(patch)
cap = cv2.VideoCapture(0)



if not cap.isOpened():
    print("Cannot open camera")
    exit()


DURATION = 30

EDGE_TOP = 150
EDGE_RIGHT = 700
EDGE_BOTTOM = 600
EDGE_LEFT = 200


while True:

    success, img = cap.read()

    if success :

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
            # print("area : ", area)
            if area > 300 and 0 not in cnt:

                if 0 or threshold.shape[1] - 1 not in (cnt[i][0][0] for i in range(len(cnt))):

                    if 0 or threshold.shape[0] - 1 not in (cnt[i][0][1] for i in range(len(cnt))):

                        cv2.drawContours(fish_contour, [cnt], 0, 255, -1)

                        count = count + 1

        #! show frame
        print("count : " + str(count))
        cv2.imshow("Edge", img_cvtc)
        cv2.imshow("Thresh", fish_contour)
        # time.sleep(0.5)
        if cv2.waitKey(1) == ord('q'):
            break    

    

cap.release()
cv2.destroyAllWindows()
