import os
from my_models.emailNotifyModel import EmailNotify
from constant import FOLDER_SAVE_IMAGES, res_success
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session



    
def add_email_notify():
    if request.method == "POST":

        
        username = request.form.get("username")
        email = request.form.get("email")

        exist_email = EmailNotify.objects(email=email)
        
        if exist_email : 
            return 'EXIST_EMAIL'
        
       
        
        newProfile = EmailNotify(email=email,username=username)
        newProfile.save()

        

        return 'OK'
    
def get_email_notify(username):
    result = EmailNotify.objects(username=username)
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
    
def update_email_notify(username):
    
    email = request.form.get("email")
    print(email)
    exist_email = EmailNotify.objects(email=email)
    print(exist_email)
    
    if exist_email : 
        return 'EXIST_EMAIL'
    
    EmailNotify.objects(username=username).update(email=email)
    
    return 'OK'
    
def delete_email_notify(username):    
    EmailNotify.objects(username=username).delete()
    return '123123123123123'
