import os
from my_models.notificationModel import Notification
from constant import FOLDER_SAVE_IMAGES, res_success
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session



    
def add_notify():
    if request.method == "POST":

        
        username = request.form.get("username")
        text = request.form.get("text")

        
        
        newNotify = Notification(username=username, text=text)
        newNotify.save()

        

        return 'OK'
    
def get_notify(username):
    result = Notification.objects(username=username)
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
    
def update_notify(username):
    
    email = request.form.get("email")
    print(email)
    exist_email = Notification.objects(email=email)
    print(exist_email)
    
    if exist_email : 
        return 'EXIST_EMAIL'
    
    Notification.objects(username=username).update(email=email)
    
    return 'OK'
    
def delete_notify(username):    
    Notification.objects(username=username).delete()
    return 'OK'
