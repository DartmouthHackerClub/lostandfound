from flask import Flask, request, redirect, session, url_for, render_template
from flask_cas import flask_cas
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.register_blueprint(flask_cas)
app.secret_key = 'this/ought%to*be^changed'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    email = db.Column(db.String(120))

@app.route("/")
def index():
    return render_template('index.html', items=Item.query.all())

if __name__ == "__main__":
    app.run(debug=True)
