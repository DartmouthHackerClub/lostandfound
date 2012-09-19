import urllib
import requests
from lxml import etree
from flask import Flask, request, redirect, session, url_for, escape, render_template

app = Flask(__name__)
app.secret_key = 'this/ought%to*be^changed'

CAS_URL = 'https://login.dartmouth.edu/cas/'

def recursive_dict(element):
    return element.tag, dict(map(recursive_dict, element)) or element.text

def cas_login(service):
    login_url = CAS_URL + 'login?' + urllib.urlencode(locals())
    return redirect(login_url)

def cas_validate(ticket, service):
    validate_url = CAS_URL + 'serviceValidate?' + urllib.urlencode(locals())
    r = requests.get(validate_url)
    doc = etree.fromstring(r.text)
    if 'authenticationSuccess' in doc[0].tag:
        return dict((key.replace('{http://www.yale.edu/tp/cas}', ''), value) for \
                key, value in recursive_dict(doc[0])[1].items())
    return None

@app.route("/login/")
def login():
    callback_url = request.url.split('?')[0]
    if 'ticket' in request.args:
        session['user'] = cas_validate(request.args['ticket'], callback_url)
    else:
        return cas_login(callback_url)
    return redirect(url_for('index'))

@app.route("/logout/")
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
