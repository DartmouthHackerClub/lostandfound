import os
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import secure_filename
from flask_cas import flask_cas, login_required

app = Flask(__name__)
app.config.from_pyfile('local_settings.py')
app.register_blueprint(flask_cas)
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    email = db.Column(db.String(120))

    def image_url(self):
        if app.debug:
            return url_for('image', filename=self.image)
        else:
            return '/images/%s' % self.image

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in set(['png', 'jpg', 'jpeg'])

def get_email(user):
    return user['netid'] + '@kiewit.dartmouth.edu'

@app.route("/add/", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        image = request.files.get('image', None)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
            if not os.path.isdir(image_dir):
                os.makedirs(image_dir)
            image.save(os.path.join(image_dir, filename))
            item = Item()
            item.email = get_email(session['user'])
            item.image = filename
            db.session.add(item)
            db.session.commit()
    return render_template('add.html')

if app.debug:
    @app.route("/images/<filename>")
    @login_required
    def image(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/item/<int:item_id>/")
@login_required
def item(item_id):
    return render_template('item.html', item=Item.query.get(item_id))

@app.route("/")
@login_required
def index():
    return render_template('index.html', items=Item.query.all())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.debug, port=5001)
