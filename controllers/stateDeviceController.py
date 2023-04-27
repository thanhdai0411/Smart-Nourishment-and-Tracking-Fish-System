
from flask import Flask, render_template, Response, flash, request, redirect, url_for, session
from my_models.stateDeviceModel import StateDevice


def update_status(device) :
    print(device)

    state_form = request.form.get("state")

    state = ''

    if( not state_form) :
        state = request.get_json()['state']
    else :
        state = request.form.get("state")

    
    StateDevice.objects(device=device).update(state=state)
    
    return 'OK'

def init_status () :
    if request.method == "POST":

        device = request.get_json()['device']
        state = request.get_json()['state']

        print(device, state)
        
        
        newState = StateDevice(device=device,state=state)
        newState.save()

    
        return 'OK'

def get_status(device) :
    result = StateDevice.objects(device=device)
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