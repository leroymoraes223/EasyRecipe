from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class user(db.Model, UserMixin):
    UID = db.Column("UID", db.Integer, primary_key=True)
    USERNAME = db.Column("USERNAME", db.Text, unique=True)
    PASSWORD = db.Column("PASSWORD", db.Text)
    EMAIL = db.Column("EMAIL", db.Text, unique=True)
    post = db.Relationship("post")

    def __init__(self, USERNAME, PASSWORD, EMAIL):
        self.USERNAME = USERNAME
        self.PASSWORD = PASSWORD
        self.EMAIL = EMAIL

    def get_id(self):
        return self.UID


class post(db.Model):
    PID = db.Column("PID", db.Integer, primary_key=True)
    TITLE = db.Column("TITLE", db.String(100))
    PD = db.Column("PD", db.Text)
    ING = db.Column("ING", db.Text)
    NUTRI = db.Column("NUTRI", db.Text)
    RECIPE = db.Column("RECIPE", db.Text)
    DATE = db.Column("DATE", db.DateTime(timezone=True), default=func.now())
    UID = db.Column("UID", db.Integer, db.ForeignKey(user.UID))
    img = db.Relationship("img")

    def __init__(self, TITLE, PD, ING, NUTRI, RECIPE, UID):
        self.TITLE = TITLE
        self.PD = PD
        self.ING = ING
        self.NUTRI = NUTRI
        self.RECIPE = RECIPE
        self.UID = UID


class img(db.Model):
    IID = db.Column("IID", db.Integer, primary_key=True)
    bufferdata = db.Column("bufferdata", db.Text, unique=True, nullable=False)
    NAME = db.Column("NAME", db.Text, nullable=False)
    mimetype = db.Column("mimetype", db.Text, nullable=False)
    PID = db.Column("PID",db.Integer, db.ForeignKey(post.PID))

    def __init__(self, NAME, bufferdata, mimetype, PID):
        self.NAME = NAME
        self.bufferdata = bufferdata
        self.mimetype = mimetype
        self.PID = PID
