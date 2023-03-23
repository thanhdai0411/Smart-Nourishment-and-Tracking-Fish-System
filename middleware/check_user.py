from flask import session, redirect


def check_user():
    if not session.get('username'):
        return redirect('/')
    return redirect('/home')
