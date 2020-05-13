#!/usr/bin/python
from flask import Flask, request, redirect, jsonify, send_file, make_response
from json import loads
from AuthAndData import *
import re

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
auth = Authenticator()
app = Flask(__name__, static_url_path='/assets/')


@app.route('/Sign-up.html')
def signup_html():
    if getuser():
        return redirect('/Home.html')
    return send_file('Sandbox/Sign-up.html')


@app.route('/Home.html')
def home_html():
    if getuser():
        return send_file('Sandbox/Home.html')
    return redirect('/Sign-in.html')


@app.route('/Sign-in.html')
def signin_html():
    if getuser():
        return redirect('/Home.html')
    return send_file('Sandbox/Sign-in.html')


@app.route('/Conversation.html')
def conversation():
    if getuser():
        return send_file('Sandbox/Conversation.html')
    return redirect('/Sign-in.html')


@app.route('/')
def testing():
    return redirect('/Home.html')


@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.ico')


def getuser():
    return auth.sessidtouser(request.cookies.get('sessid'))


@app.route('/register', methods=['POST'])
def registeruser():
    data = loads(request.data)
    err = auth.register(data)
    if err == 0:
        return '', 200
    else:
        error = {'confirm': None, 'password': None, 'username': None, 'email': None}
        if err & 1:
            error['confirm'] = "Passwords do not match"
        if err & 2:
            error['password'] = 'Password must be at least 8 characters'
        if err & 4:
            error['email'] = 'Invalid email'
        elif err & 8:
            error['email'] = 'Email in use'
        if err & 16:
            error['username'] = 'Username in use'
        elif err & 32:
            error['username'] = 'Username cannot be a valid email'
        elif err & 64:
            error['username'] = 'Empty username'
        elif err & 128:
            error['username'] = 'Username cannot contain whitespace'
        return jsonify(error), 403


@app.route('/login', methods=['POST'])
def login():
    data = loads(request.data)
    sessid = auth.authenticate(data)
    if sessid:
        resp = make_response('')
        resp.set_cookie('sessid', sessid)
        return resp
    else:
        return '', 403


@app.route('/darkmode', methods=['POST', 'GET'])
def darkmode():
    if request.method == "POST":
        auth.user_toggle_dark_mode(getuser())
    return {'darkmode': auth.user_get_dark_mode(getuser())}


@app.route('/getuserdata')
def userdata():
    return jsonify({'email': auth.users_to_emails[getuser()], 'username': auth.get_username(getuser())})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
