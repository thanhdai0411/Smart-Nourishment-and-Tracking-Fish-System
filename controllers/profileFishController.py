import os
from my_models.labelFishModel import LabelFish
from constant import FOLDER_SAVE_IMAGES, res_success
from constant import SUCCESS_STATUS, PATCH_TO_COCO12YAML, FOLDER_SAVE_LABELS, FOLDER_SAVE_IMAGES



def add_profile () : 
    return "123"
    #  if request.method == 'POST':

    #     label = request.form.get('label')
    #     coordinates = request.form.get('coordinates')
    #     image_name = request.form.get('image_name')
    #     username = request.form.get('username')
    #     if(not label or not coordinates or not image_name or not username):
    #         return 'FAIL_NOT'

    #     img = request.files['file']

    #     for images in os.listdir(FOLDER_SAVE_IMAGES):
    #         if(images == secure_filename(label + '_' + img.filename)):
    #             return 'FAIL'

    #     state = addLabelForTrainModel(label, coordinates, img, image_name, username)

    #     return 'ok'
    # return None