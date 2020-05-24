#!/usr/bin/python
from flask import Flask, request, redirect, jsonify, send_file, make_response, render_template
from json import loads
from AuthAndData import *
import re

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
auth = Authenticator()
app = Flask(__name__, static_url_path='/assets/', template_folder='Sandbox')


@app.route('/Sign-up.html')
def signup_html():
    if getuser():
        return redirect('/Home.html')
    return send_file('Sandbox/Sign-up.html')


@app.route('/Home.html')
def home_html():
    if getuser():
        return render_template('Home.html', email=auth.users_to_emails[getuser()],
                               username=auth.get_username(getuser()), darkmode=auth.user_get_dark_mode(getuser()))
    return redirect('/Sign-in.html')


@app.route('/Sign-in.html')
def signin_html():
    if getuser():
        return redirect('/Home.html')
    return send_file('Sandbox/Sign-in.html')


@app.route('/Conversation.html')
def conversation():
    if getuser():
        return render_template('Conversation.html', darkmode=auth.user_get_dark_mode(getuser()), username=getuser())
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
    sessid = auth.register(data)
    if type(sessid) == str:
        resp = make_response('')
        resp.set_cookie('sessid', sessid)
        return resp
    if type(sessid) == bool:
        return '', 400
    else:
        return jsonify(sessid), 403


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
    try:
        if request.method == "POST":
            auth.user_toggle_dark_mode(getuser())
        return {'darkmode': auth.user_get_dark_mode(getuser())}
    except KeyError:
        return '{}', 403


@app.route('/getuserdata')
def userdata():
    try:
        return jsonify({'email': auth.users_to_emails[getuser()], 'username': auth.get_username(getuser())})
    except KeyError:
        return '{}', 403


@app.route('/signout', methods=['POST'])
def signout():
    auth.deauthenticate(request.cookies.get('sessid'))
    resp = redirect('/Sign-in.html')
    resp.set_cookie('sessid', '', max_age=0)
    return resp


@app.route('/Conversations/getall')
def getconvos():
    try:
        return jsonify(auth.get_user_conversation_info(getuser()))
    except KeyError:
        return '', 403


@app.route('/Conversations/new', methods=['POST'])
def newconvo():
    data = loads(request.data)
    if not auth.add_conversation(getuser(), data['email']):
        return '', 403
    return jsonify(auth.get_user_conversation_info(getuser()))


@app.route('/conversations/<cid>', methods=['POLL', 'POST', 'DELETE'])
def conversation_manage(cid):
    try:
        if request.method == 'POLL':
            return jsonify(auth.user_get_conversation(getuser(), cid)[loads(request.data)['no_of_convos']:])
        elif request.method == 'POST':
            auth.user_conversation_add_comment(getuser(), cid, loads(request.data)['comment'])
            return jsonify(auth.user_get_conversation(getuser(), cid)[loads(request.data)['no_of_convos']:])
        elif request.method == 'DELETE':
            auth.user_delete_conversation(getuser(), cid)
            return jsonify(auth.get_user_conversation_info(getuser()))
    except KeyError:
        return '', 403


@app.route('/deluser')
def deluser():
    raise NotImplementedError


@app.route('/getblocked')
def getblocked():
    raise NotImplementedError


@app.route('/block')
def blockuser():
    raise NotImplementedError


@app.route('/secretquestion', methods=['GET', 'PUT'])
def set_secret_question():
    raise NotImplementedError


@app.route('/changepassword', methods=['POST'])
def changepassword():
    raise NotImplementedError


@app.route('/resetpassword', methods=['POST'])
def resetpassword():
    raise NotImplementedError


@app.route('/Settings.html')
def settingspage():
    return send_file('Sandbox/Settings.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
