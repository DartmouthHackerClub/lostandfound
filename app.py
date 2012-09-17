import pprint
import urllib
import requests
from flask import Flask, request, redirect, session, url_for, escape, render_template

app = Flask(__name__)
app.secret_key = 'this/ought%to*be^changed'

CAS_URL = 'https://login.dartmouth.edu/cas/'

def cas_login(service):
    '''
    Get an auth ticket by redirecting to the cas login page.
    '''
    login_url = CAS_URL + 'login?' + urllib.urlencode(locals())
    return redirect(login_url)

def cas_validate(ticket, service):
    '''
    Validate the auth ticket and redirect back to the application.
    '''
    validate_url = CAS_URL + 'validate?' + urllib.urlencode(locals())
    r = requests.get(validate_url)
    if 'yes' in r.text:
        return r.text.splitlines()[-1]
    return None

@app.route("/login/")
def login():
    callback_url = request.url.split('?')[0]
    if 'ticket' in request.args:
        session['username'] = cas_validate(request.args['ticket'], callback_url)
    else:
        return cas_login(callback_url)
    return redirect(url_for('index'))

@app.route("/logout/")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
