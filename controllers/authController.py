
from flask import request, redirect, jsonify, render_template, session
from flask_session import Session

from constant import SUCCESS_STATUS, ERROR_STATUS, fail_status, success_status
from models.userModel import User

#  query ==> request.args
#  form  ==> request.form

LOGIN_SUCCESS = 1
REGISTER_SUCCESS = 2


def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    password_again = request.form.get('password_again')
    try:

        if not username:
            return fail_status("Please enter username")

        usernameExist = User.objects(username=username).first()
        if username == usernameExist:
            return fail_status("Username exist")

        if password_again != password:
            return fail_status("Password again not match")

        newUser = User(username=username, password=password)
        newUser.save()
        session['login'] = True
        session['username'] = username
        return redirect('/home')

    except ValueError as ve:
        return fail_status(ve)


def login_user():
    username = request.form.get('username')
    password = request.form.get('password')
    try:
        if not username or not password:
            return fail_status("Please enter username")

        user = User.objects(username=username).first()

        if not user:
            return fail_status("User not exist")

        if user.password != password:
            return fail_status("Password enter not match")

        session['login'] = True
        session['username'] = username
        # return user.to_json()
        # return render_template('home_page.html', auth=REGISTER_SUCCESS)
        return redirect('/home')

    except ValueError as ve:
        return fail_status(ve)


def logout():
    session.pop('login', None)
    session.pop('username', None)
    return redirect("/")


def get_user(username):
    try:
        user = User.objects(username=username).first()
        print(user.to_json())

        return SUCCESS_STATUS
    except ValueError as ve:
        print("Err: ", ve)
        return ERROR_STATUS

    # User.objects(name="Thssanh Dai").first()
