#!/usr/bin/python
import html
from flask import Flask, request, make_response, redirect, jsonify, send_file, abort
from json import loads, dumps
from AuthFrameWork import Authenticator
from CSRFToken import CSRFTokenHandler
from errors import *
from copy import deepcopy
import re
from DataHandler import DataHandler

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')
csrf_handler = CSRFTokenHandler()
auth = Authenticator()
auth.register({"password": "noobism!", "username": "yeet", "email": "rohroexperiment@gmail.com"})
auth.register({"password": "noobism!", "username": "yeet2", "email": "rohroexperimenter@gmail.com"})
datahandler = DataHandler()
datahandler.adduser('yeet')
datahandler.adduser('yeet2')
datahandler.add_conversation('yeet', 'yeet2', 'yeeters')
datahandler.add_conversation('yeet', 'yeet2', 'yeeters')
datahandler.add_conversation('yeet', 'yeet2', 'yeeters')
datahandler.add_conversation('yeet', 'yeet2', 'yeeters')
app = Flask(__name__, static_url_path='/assets/')
csrf_html_response = """
    <!DOCTYPE html>
    <html>
    <head>
    <title> CSRF Verification failed</title>
    <meta charset='utf-8'/>
    </head>
    <body>
    <h1> CSRF verification failed</h1>
    <p> We could not verify the authenticity of your request and authentication has failed </p>
    </body>
    </html>
    """


def getuser():
    return auth.sessidtouser(request.cookies.get('sessid'))


@app.route('/csrf_token')
def gen_csrftok():
    tok = csrf_handler.gentok()
    resp = make_response('')
    resp.set_cookie('csrf_token', tok, max_age=86400)
    return resp


@app.route('/register', methods=['POST'])
def registeruser():
    response = deepcopy(register_errors_template)
    error = False
    if csrf_verify():
        data = loads(request.data)
        email = data.get('email')
        username = data.get('username')
        confirm = data.get('confirm')
        passwd = data.get('password')
        if not username:
            response['errors']['username'] = "Empty username"
            error = True
        username = html.escape(username.lower().strip())
        if not username:
            response['errors']['username'] = "Empty username"
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
            resp = make_response(dumps(register_success_template))
            resp.set_cookie('sessid', auth.authenticate(data), max_age=86400)
            return resp
    else:
        response['csrf'] = True
        return dumps(response)


def csrf_verify():
    csrf_tok = request.headers.get('X-CSRF-Token')
    return bool(csrf_tok) and csrf_handler.validatetok(csrf_tok)


@app.route('/csrf_fail')
def csrf_fail():
    return csrf_html_response


def isvalidemail(email):
    return bool(email_regex.match(email))


@app.route('/verify_csrftok')
def verifytok():
    csrf_tok = request.data
    return dumps({'valid': bool(csrf_tok) and csrf_handler.validatetok(csrf_tok)})


@app.route('/login', methods=['POST'])
def authenticate():
    if csrf_verify():
        data = loads(request.data)
        if True in (not data.get('username'), not data.get('password')):
            return dumps({'status': 'error', 'csrf': False})
        data['username'] = data['username'].strip().lower()
        sessid = auth.authenticate(data)
        if sessid:
            resp = make_response(dumps({'status': 'success'}))
            resp.set_cookie('sessid', sessid)
            return resp
        else:
            return dumps({'status': 'error', 'csrf': False})
    else:
        return dumps({'status': 'error', 'csrf': True})


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
    resp = redirect('/')
    resp.set_cookie('sessid', '', max_age=0)
    return resp


@app.route('/Conversations/new', methods=['POST'])
def newconversation():
    if csrf_verify():
        data = loads(request.data)
        if getuser() != auth.emails_to_users[data['email']]:
            datahandler.add_conversation(getuser(),
                                         auth.emails_to_users[data['email']], data['name'])
    else:
        abort(403)
    return dumps(datahandler.user_get_conversation_info(getuser()))


@app.route('/Conversations/getall')
def getconvos():
    return dumps(datahandler.user_get_conversation_info(getuser()))


@app.route('/conversations/<cid>', methods=['POLL', 'GET', 'POST', 'DELETE'])
def conversation_manage(cid):
    if request.method == 'POLL':
        abort(501)
    elif request.method == 'GET':
        return jsonify(datahandler.user_get_conversation(getuser(), cid))
    elif request.method == 'POST':
        datahandler.user_conversation_add_comment(getuser(), cid,
                                                  loads(request.data)['comment'])
        return jsonify(datahandler.user_get_conversation(getuser(), cid))
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
    app.run(debug=True)
