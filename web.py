from flask import Flask, request, make_response, redirect, jsonify
from json import loads
from AuthFrameWork import Authenticator
from CSRFToken import CSRFTokenHandler
from errors import *
from copy import deepcopy
import re

email_regex = re.compile('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$')

csrf_handler = CSRFTokenHandler()
auth = Authenticator()
app = Flask(__name__)
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
    resp.set_cookie('csrf_token', tok)
    return resp


@app.route('/register')
def registeruser():
    response = deepcopy(register_errors_template)
    error = False
    if csrf_verify():
        data = loads(request.data)
        email = data.get('email')
        username = data.get('username')
        confirm = data.get('confirm')
        passwd = data.get('password')
        if not email:
            response['errors']['email'] = "Empty email"
            error = True
        if not confirm:
            response['errors']['confirm'] = "Empty confirm"
            error = True
        if not username:
            response['errors']['username'] = "Empty username"
            error = True
        if not passwd:
            response['errors']['password'] = "Empty password"
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
        if error:
            return jsonify(response)
        else:
            auth.register(data)
            resp = jsonify(register_success_template)
            resp.set_cookie('sessid', auth.authenticate(data))
            return resp
    else:
        response['csrf'] = True
        return jsonify(response)


def csrf_verify():
    csrf_tok = request.headers.get('X-CSRF-Token')
    return not csrf_tok and csrf_handler.validatetok(csrf_tok)


@app.route('/csrf_fail')
def csrf_fail():
    return csrf_html_response

def isvalidemail(email):
    return bool(email_regex.match(email))

if __name__ == '__main__':
    app.run()
