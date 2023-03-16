import os
from my_models.statusTrainModel import StatusTrain
from constant import FOLDER_SAVE_IMAGES, res_success


def get_status_train(username):
    result = StatusTrain.objects(username=username)
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


def delete_status_train(username):
    StatusTrain.objects(username=username).delete()
    return 'ok'
    
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


