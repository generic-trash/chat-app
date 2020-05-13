#!/usr/bin/python
from flask import Flask, request, make_response, redirect, jsonify, send_file, abort
from json import loads
from AuthFrameWork import Authenticator
from errors import *
from copy import deepcopy
import re
from DataHandler import DataHandler

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
auth = Authenticator()
datahandler = DataHandler()
app = Flask(__name__, static_url_path='/assets/')


def getuser():
    return auth.sessidtouser(request.cookies.get('sessid'))


@app.route('/register', methods=['POST'])
def registeruser():
    response = deepcopy(register_errors_template)
    error = False
    data = loads(request.data)
    email = data.get('email').strip()
    username = data.get('username').strip().lower()
    confirm = data.get('confirm')
    passwd = data.get('password')
    if not username:
        response['errors']['username'] = "Empty username"
        error = True
    if isvalidemail(username):
        response['errors']['username'] = "Username cannot be an email address"
        error = True
    if ' ' in username or '\t' in username:
        response['errors']['username'] = "Username cannot contain whitespace"
        error = True
    if auth.userexists(username):
        response['errors']['username'] = "Username in use"
        error = True
    if auth.emailexists(email):
        response['errors']['email'] = "Email in use"
        error = True
    if not isvalidemail(email):
        response['errors']['email'] = "Invalid email"
        error = True
    if confirm != passwd:
        response['errors']['confirm'] = "Passwords do not match"
        error = True
    if len(passwd) < 8 or sum(c.isdigit() for c in passwd) < 2:
        response['errors']['password'] = "There must be at least 8 characters and 2 numbers"
        error = True
    if error:
        return jsonify(response)
    else:
        auth.register(data)
        datahandler.adduser(data.get('username'))
        resp = jsonify(register_success_template)
        resp.set_cookie('sessid', auth.authenticate(data), max_age=86400)
        return resp


def isvalidemail(email):
    return bool(email_regex.match(email))


@app.route('/login', methods=['POST'])
def authenticate():
    data = loads(request.data)
    if True in (not data.get('username'), not data.get('password')):
        return jsonify({'status': 'error'})
    data['username'] = data['username'].strip().lower()
    if auth.emailexists(data['username']):
        data['username'] = auth.emails_to_users[data['username']]
    sessid = auth.authenticate(data)
    if sessid:
        resp = make_response(jsonify({'status': 'success'}))
        resp.set_cookie('sessid', sessid)
        return resp
    else:
        return jsonify({'status': 'error'})


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


@app.route('/signout', methods=['POST'])
def signout():
    auth.deauthenticate(request.cookies.get('sessid'))
    resp = redirect('/Sign-in.html')
    resp.set_cookie('sessid', '', max_age=0)
    return resp


@app.route('/Conversations/new', methods=['POST'])
def newconversation():
    data = loads(request.data)
    if auth.userexists(data['email']):
        data['email'] = auth.users_to_emails[data['email']]
    if getuser() != auth.emails_to_users[data['email']]:
        datahandler.add_conversation(getuser(),
                                     auth.emails_to_users[data['email']])
    return jsonify(datahandler.user_get_conversation_info(getuser()))


@app.route('/Conversations/getall')
def getconvos():
    return jsonify(datahandler.user_get_conversation_info(getuser()))


@app.route('/conversations/<cid>', methods=['POLL', 'POST', 'DELETE'])
def conversation_manage(cid):
    if request.method == 'POLL':
        return jsonify(datahandler.user_get_conversation(getuser(), cid)[loads(request.data)['no_of_convos']:])
    elif request.method == 'POST':
        datahandler.user_conversation_add_comment(getuser(), cid,
                                                  loads(request.data)['comment'])
        return jsonify(datahandler.user_get_conversation(getuser(), cid)[loads(request.data)['no_of_convos']:])
    elif request.method == 'DELETE':
        datahandler.user_delete_conversation(getuser(), cid)
        return jsonify(datahandler.user_get_conversation_info(getuser()))


@app.route('/getuserdata')
def getuserdata():
    return jsonify({'username': datahandler.get_username(getuser()), 'email': auth.users_to_emails[getuser()]})


@app.route('/darkmode', methods=['POST', 'GET'])
def getdarkmode():
    if request.method == 'POST':
        datahandler.user_toggle_dark_mode(getuser())
    return jsonify({'darkmode': datahandler.user_get_dark_mode(getuser())})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
