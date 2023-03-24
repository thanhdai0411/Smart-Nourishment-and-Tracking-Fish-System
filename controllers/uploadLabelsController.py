
from datetime import datetime
from turtle import title
from flask import Flask, render_template, Response, flash, request, redirect, url_for
from constant import SUCCESS_STATUS, PATCH_TO_COCO12YAML, FOLDER_SAVE_LABELS, FOLDER_SAVE_IMAGES
import os.path
from os import listdir
import threading
from subprocess import call

from werkzeug.utils import secure_filename

from my_utils.addLabelForTrainModel import addLabelForTrainModel
from my_models.labelFishModel import LabelFish
import json


def upload_labels():

    if request.method == 'POST':

        label = request.form.get('label')
        coordinates = request.form.get('coordinates')
        image_name = request.form.get('image_name')
        username = request.form.get('username')

        print(label, username)
        LIMIT_LABEL = 5
        result = LabelFish.objects(username=username)
        lengthLabel = len(json.loads(result.to_json()))

        if lengthLabel == LIMIT_LABEL :
            return "LIMIT_LABEL"



        if(not label or not coordinates or not image_name or not username):
            return 'FAIL_NOT'

        img = request.files['file']

        for images in os.listdir(FOLDER_SAVE_IMAGES):
            if(images == secure_filename(label + '_' + img.filename)):
                return 'FAIL'

        state = addLabelForTrainModel(label, coordinates, img, image_name, username)
        if state : 
            print("state: ", str(state) )
            return state
        else :
            return 'ok'
    return None
