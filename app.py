import os
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory, abort
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cas import flask_cas, login_required

app = Flask(__name__)
app.config.from_pyfile('local_settings.py')
app.register_blueprint(flask_cas)
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))
    email = db.Column(db.String(120))
    claimed = db.Column(db.Boolean, default=False)

    def image_url(self):
        if app.debug:
            return url_for('image', filename=self.image)
        else:
            return '/images/%s' % self.image

    def __repr__(self):
        return "Item %s" % (self.id)

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
            image_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
            if not os.path.isdir(image_dir):
                os.makedirs(image_dir)
            item = Item()
            item.email = get_email(session['user'])
            db.session.add(item)
            db.session.commit()
            filename = "%s.%s" % (item.id, image.filename.rsplit('.')[-1])
            image.save(os.path.join(image_dir, filename))
            item.image = filename
            db.session.commit()
    return render_template('add.html')

if app.debug:
    @app.route("/images/<filename>")
    @login_required
    def image(filename):
        image_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'images')
        return send_from_directory(image_dir, filename)

@app.route("/item/<int:item_id>/claim/")
@login_required
def claim_item(item_id):
    item = Item.query.get(item_id)
    item.claimed = not item.claimed
    db.session.commit()
    return redirect(url_for('item', item_id=item_id))

@app.route("/item/<int:item_id>/")
@login_required
def item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        abort(404)
    return render_template('item.html', item=item, get_email=get_email)

@app.route("/")
@login_required
def index():
    return render_template('index.html', items=Item.query.filter_by(claimed=False))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.debug, port=5001)
