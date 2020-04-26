from flask import Flask, request, make_response, redirect, jsonify, send_file
from json import loads, dumps
from AuthFrameWork import Authenticator
from CSRFToken import CSRFTokenHandler
from errors import *
from copy import deepcopy
import re

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

csrf_handler = CSRFTokenHandler()
auth = Authenticator()
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


@app.route('/csrf_token')
def gen_csrftok():
    tok = csrf_handler.gentok()
    resp = jsonify({'token': tok})
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


@app.route('/getuser')
def whoami():
    x = auth.sessidtouser(request.cookies.get('sessid'))
    return x if x else "<h1>NOT LOGGED IN!!! </h1>"


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
    if auth.sessidtouser(request.cookies.get('sessid')):
        return redirect('/Home.html')
    return send_file('Sandbox/Sign-up.html')

@app.route('/Home.html')
def home_html():
    if auth.sessidtouser(request.cookies.get('sessid')):
        return send_file('Sandbox/Home.html')
    return redirect('/Sign-in.html')

@app.route('/Sign-in.html')
def signin_html():
    if auth.sessidtouser(request.cookies.get('sessid')):
        return redirect('/Home.html')
    return send_file('Sandbox/Sign-in.html')

@app.route('/Conversation.html')
def conversation():
    if auth.sessidtouser(request.cookies.get('sessid')):
        return send_file('Sandbox/Conversation.html')

@app.route('/')
def testing():
    return send_file('Sandbox/Home.html')


if __name__ == '__main__':
    app.run(debug=True)
