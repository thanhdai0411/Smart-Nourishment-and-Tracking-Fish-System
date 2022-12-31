from constant import FOLDER_SAVE_IMAGES, PATCH_TO_COCO12YAML, FOLDER_SAVE_LABELS


import os
from werkzeug.utils import secure_filename


# fileNameLabelImage = label + '_' + img.filename
from my_models.labelFishModel import LabelFish
from my_models.userModel import User


def saveLabelToDB(username, label):
    user = User.objects(username=username).first()
    LabelFish(name=label, user_id=user.id, username=username).save()


def addLabelFileCoCo128(imageFromUserName, coordinate, index):
    coor = str(index) + coordinate

    completeName = os.path.join(
        FOLDER_SAVE_LABELS, imageFromUserName + ".txt")

    file1 = open(completeName, "w")
    file1.write(coor)
    file1.close()


def addImageForCoCo128(imgFromUser, newLabel):

    for images in os.listdir(FOLDER_SAVE_IMAGES):
        if(images == secure_filename(newLabel + '_' + imgFromUser.filename)):
            return 'FAIL'

    imgFromUser.save(os.path.join(FOLDER_SAVE_IMAGES,
                                  secure_filename(newLabel + '_' + imgFromUser.filename)))


def addLabelForTrainModel(newLabel, coordinate, imgFromUser, imageFromUserName, username):

    WHITE_SPACE = "    "
    nameFile = newLabel + '_' + imageFromUserName

    saveCoco128Read = open(PATCH_TO_COCO12YAML, 'r')

    a = saveCoco128Read.read()

    if a:

        b = a.split("\n")
        b.pop()

        c = len(b)
        d = b[c - 1]

        e = d.split(":")

        f = e[0].strip()
        g = e[1].strip()

        listLabel = b[3:]

        arr = []
        for item in listLabel:

            e = item.split(":")
            label = e[1].strip()
            arr.append(label)

        exist = False
        for value in arr:
            if value == newLabel:
                exist = True

        if exist:
            print("exist item. Save label file")
            addLabelFileCoCo128(nameFile, coordinate, f + " ")
            addImageForCoCo128(imgFromUser, newLabel)
        else:
            add = WHITE_SPACE + str(int(f) + 1) + ": " + newLabel
            saveLabelToDB(username, newLabel)

            addLabelFileCoCo128(nameFile,
                                coordinate, str(int(f) + 1) + " ")

            addImageForCoCo128(imgFromUser, newLabel)

            b.append(add)
            # print(b)
            print(b)

            saveCoco128Write = open(PATCH_TO_COCO12YAML, 'w')
            for value in b:
                saveCoco128Write.write(value)
                saveCoco128Write.write('\n')
            saveCoco128Write.close()
    else:
        saveCoco128Write = open(PATCH_TO_COCO12YAML, 'w')

        addLabelFileCoCo128(nameFile, coordinate, 0 + " ")
        addImageForCoCo128(imgFromUser, newLabel)

        saveLabelToDB(username, newLabel)

        coco128 = [
            'train: ' + FOLDER_SAVE_IMAGES, 'val: ' + FOLDER_SAVE_IMAGES, 'names:', WHITE_SPACE + '0: ' + newLabel]
        for value in coco128:
            saveCoco128Write.write(value)
            saveCoco128Write.write('\n')
        saveCoco128Write.close()
