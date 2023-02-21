import os
from my_models.labelFishModel import LabelFish
from constant import FOLDER_SAVE_IMAGES, res_success


def get_fish(username):
    result = LabelFish.objects(username=username)
    try:
        return {
            "success": 1,
            'data': result.to_json(),
            'message': 'success'
        }
    except(Exception):
        return {
            "success": 0,
            'message': Exception,
        }


def delete_fish(username, fish_name):
    result = LabelFish.objects(username=username, name=fish_name)
    print(result)
    return result
    
    # try:
    #     return {
    #         "success": 1,
    #         'data': result.to_json(),
    #         'message': 'success'
    #     }
    # except(Exception):
    #     return {
    #         "success": 0,
    #         'message': Exception,
    #     }


def get_data_present(fish_name):
    try:
        count = 0
        for images in os.listdir(FOLDER_SAVE_IMAGES):
            if(images.split("_")[0] == fish_name):
                count = count + 1
        return res_success("success", count)

    except(Exception):
        return {
            "success": 0,
            'message': Exception,
        }
