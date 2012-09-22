import os
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from flask_cas import flask_cas

UPLOAD_FOLDER = '/tmp/lostandfound/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.register_blueprint(flask_cas)
app.secret_key = 'this/ought%to*be^changed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    email = db.Column(db.String(120))

    def image_url(self):
        if self.image:
            return url_for('image', filename=self.image)
        else:
            return 'http://lorempixel.com/400/200'

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_email(user):
    return user['netid'] + '@kiewit.dartmouth.edu'

@app.route("/add/", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        image = request.files.get('image', None)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item = Item()
            db.session.add(item)
            db.session.commit()
    return render_template('add.html')

@app.route("/images/<filename>")
def image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/item/<int:item_id>/")
def item(item_id):
    return item_id

@app.route("/")
def index():
    return render_template('index.html', items=Item.query.all())

if __name__ == "__main__":
    app.run(debug=True)
