from my_models.foodModel import Food
from flask import request, redirect, jsonify, render_template, session
from constant import SUCCESS_STATUS, ERROR_STATUS, PATCH_FOOD_SETTING, fail_status, success_status
import json


def add_food():
    if request.method == 'POST':
        try:
            time = request.form.get('time')
            username = request.form.get('username')
            amount_food = request.form.get('amount_food')
            result = Food.objects(username=username)
            lengthSetting = len(json.loads(result.to_json()))
            for food in result:
                print(food.time)
                if time == food.time:
                    return 'EXIST_TIME'

            if lengthSetting == 10:
                return 'LIMIT'

            if not time or not amount_food or not username:
                return fail_status("Not enough setting food")
            print(time, username, amount_food)
            newFood = Food(username=username, amount_food=amount_food, time=time)
            newFood.save()

            return 'OK'

        except ValueError as ve:
            return 'FAIL'
    else:
        return None


def get_food(username):
    result = Food.objects(username=username)

    # f = open(PATCH_FOOD_SETTING, "w")
    with open(PATCH_FOOD_SETTING, "w") as outfile:
        # json.dump(result.to_json(), outfile)
        print("write json")
        outfile.write(result.to_json())
    # f.write(result.to_json())
    # f.close()

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


def delete_food(id):
    food = Food.objects(id=id)

    try:
        food.delete()
        return {
            "success": 1,
            'message': 'success'
        }
    except(Exception):
        return {
            "success": 0,
            'message': Exception,
        }

def update_food(id):
    if request.method == 'POST':
        try:
            food = Food.objects(id=id)

            time = request.form.get('time')
            amount_food = request.form.get('amount_food')

            food.update(time=time, amount_food=amount_food, status="WAITING")

            return 'OK'

        except ValueError as ve:
            return 'FAIL'
    else:
        return None


def update_food_daily():
    if request.method == 'POST':
        try:
            food = Food.objects()

            food.update(status="WAITING")

            return 'OK'

        except ValueError as ve:
            return 'FAIL'
    else:
        return None


def update_food_status(id):
    if request.method == 'POST':
        try:
            food = Food.objects(id=id)

            status = request.form.get('status')

            food.update(status=status)

            return 'OK'

        except ValueError as ve:
            return 'FAIL'
    else:
        return None
