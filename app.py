from flask import Flask, request, redirect, session, url_for, render_template
from flask_cas import flask_cas

app = Flask(__name__)
app.register_blueprint(flask_cas)
app.secret_key = 'this/ought%to*be^changed'

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
