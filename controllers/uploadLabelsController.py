
from datetime import datetime
from turtle import title
from flask import Flask, render_template, Response, flash, request, redirect, url_for
from constant import SUCCESS_STATUS, PATCH_TO_COCO12YAML, FOLDER_SAVE_LABELS, FOLDER_SAVE_IMAGES
import os.path
from os import listdir
import threading
from subprocess import call

# from models.statusTrainModel import StatusTrain
# from models.labelFishModel import LabelFish
# from models.userModel import User

from werkzeug.utils import secure_filename


def upload_labels():

    if request.method == 'POST':

        label = request.form.get('label')
        coordinates = request.form.get('coordinates')
        image_name = request.form.get('image_name')
        username = request.form.get('username')

        img = request.files['file']
        # img = secure_filename(img.filename)

        print(img.filename, label, image_name, coordinates, username)

        for images in os.listdir(FOLDER_SAVE_IMAGES):

            # if (images.endswith(".png")):
            if(images == secure_filename(img.filename)):
                print('Trug')
                return 'FAIL'

        completeName = os.path.join(
            FOLDER_SAVE_LABELS, image_name + ".txt")

        file1 = open(completeName, "w")
        file1.write(coordinates)
        file1.close()

        img.save(os.path.join(FOLDER_SAVE_IMAGES,
                 secure_filename(img.filename)))

        coco128 = [
            'train: ' + FOLDER_SAVE_IMAGES, 'val: ' + FOLDER_SAVE_IMAGES, 'names:', '    0: ' + label]
        with open(PATCH_TO_COCO12YAML, 'w') as f:
            for value in coco128:
                f.write(value)
                f.write('\n')

        return 'ok'
    return None

    # user = User.objects(username=username).first()
    # LabelFish(name=label, user_id=user.id).save()


def train_model():
    timeCurrent = datetime.now()
    print("Time_start_train: " + str(timeCurrent))
    # StatusTrain(dateStart=str(timeCurrent),
    #             title="Start").save()
    # call('start /wait python F:\\Studyspace\\DoAn\\Aquarium\\yolov5\\train.py', shell=True)
    call(['python', 'F:\\Studyspace\\DoAn\\Aquarium\\train.py'])

    # status = StatusTrain.objects(title="Start")
    timeComplete = datetime.now()
    print("Time_end_train: " + str(timeComplete))
    # status.update(dateEnd=str(timeComplete),
    #               title="End")

    return "Train model success"
