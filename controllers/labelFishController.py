from models.labelFishModel import LabelFish


def get_fish(user_id):
    result = LabelFish.objects(user_id=user_id)
    return {
        "success": 1,
        'data': result.to_json()
    }
