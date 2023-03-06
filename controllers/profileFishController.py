import os
from constant import FOLDER_SAVE_IMAGES, res_success, fail_status, success_status
from constant import SUCCESS_STATUS, PATCH_TO_COCO12YAML, FOLDER_SAVE_LABELS, FOLDER_SAVE_IMAGES
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session

from my_models.profileFishModel import ProfileFish

from bson.objectid import ObjectId



from constant import CLOUDINARY_NAME,CLOUDINARY_API_KEY,CLOUDINARY_API_SECRET
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name=CLOUDINARY_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

def add_profile():
    if request.method == "POST":

        
        image = request.files["avatar_fish"]
        user_system = request.form.get("user_system")
        username = request.form.get("username")
        fish_type = request.form.get("fish_type")
        time_start_farming = request.form.get("time_start_farming")
        fish_name = request.form.get("fish_name")
        note = request.form.get("note")


        exist_fish_name = ProfileFish.objects(fish_name=fish_name)
        
        if exist_fish_name : 
            return 'EXIST_FISH_NAME'
        
        if not username or not fish_type or not time_start_farming or not fish_name:
            return fail_status("Not enough data")
        
        upload_result = cloudinary.uploader.upload(image)
        newProfile = ProfileFish(user_system=user_system,username=username, fish_type=fish_type, time_start_farming=time_start_farming, fish_name=fish_name, note=note.strip(), avatar = upload_result["secure_url"])
        newProfile.save()

        

        return 'OK'
        
def get_profile(username) : 
    result = ProfileFish.objects(user_system=username)
    return render_template('home_page.html', data = result )
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

def get_profile_detail(id) :
    result = ProfileFish.objects(id=id)
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

def update_profile(id) :

    image = request.files["avatar_fish_update"]
    username = request.form.get("username")
    avatar = request.form.get("avatar")
    fish_type = request.form.get("fish_type")
    time_start_farming = request.form.get("time_start_farming")
    note = request.form.get("note")

    public_id = avatar.split("/")[-1].split(".")[0]
    if image :
        cloudinary.uploader.destroy(public_id)
        upload_result = cloudinary.uploader.upload(image)
        ProfileFish.objects(id=id).update(username=username, fish_type=fish_type, time_start_farming=time_start_farming,  note=note.strip(), avatar = upload_result["secure_url"])
    else :
        ProfileFish.objects(id=id).update(username=username, fish_type=fish_type, time_start_farming=time_start_farming,  note=note.strip())

    return 'OK'

def delete_profile(id) :
    avatar = request.form.get("avatar")
    public_id = avatar.split("/")[-1].split(".")[0]
    cloudinary.uploader.destroy(public_id)
    ProfileFish.objects(id=id).delete()
    return 'OK'


