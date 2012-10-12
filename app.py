import os
from flask import Flask, request, redirect, session, url_for, render_template, send_from_directory, abort, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cas import flask_cas, login_required

app = Flask(__name__)
app.config.from_pyfile('local_settings.py')
app.register_blueprint(flask_cas)
db = SQLAlchemy(app)

claims_table = db.Table('claims',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('item_id', db.Integer, db.ForeignKey('item.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(15), unique=True)
    full_name = db.Column(db.String(200))

    found_items = db.relationship("Item", backref="finder")
    claims = db.relationship("Item", secondary=claims_table, backref="claimers")

    def __init__(self, full_name, netid):
        self.full_name = full_name
        self.netid = netid

    def email(self):
        return "%s@dartmouth.edu" % self.netid

    def __repr__(self):
        return str(self.netid)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(200))

    finder_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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

@app.before_request
def fetch_user():
    if 'user' in session:
        g.user = User.query.filter_by(netid=session['user']['netid']).first()
        if g.user is None:
            g.user = User(session['user']['name'], session['user']['netid'])
            db.session.add(g.user)
            db.session.commit()

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
            item.finder = g.user
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

@app.route("/item/<int:item_id>/claim/", methods=["POST"])
@login_required
def claim_item(item_id):
    item = Item.query.get(item_id)
    item.claimers.append(g.user)
    db.session.commit()
    return redirect(url_for('item', item_id=item_id))

@app.route("/item/<int:item_id>/unclaim", methods=["POST"])
@login_required
def unclaim_item(item_id):
    item = Item.query.get(item_id)
    item.claimers.remove(g.user)
    db.session.commit()
    return redirect(url_for('item', item_id=item_id))

@app.route("/item/<int:item_id>/")
@login_required
def item(item_id):
    item = Item.query.get(item_id)
    if item is None:
        abort(404)
    return render_template('item.html', item=item, cur_user=g.user)

@app.route("/")
@login_required
def index():
    return render_template('index.html', items=Item.query.all())

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=app.debug, port=5001)
