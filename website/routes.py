import base64
from .forms import PostUploadForm ,UserRegistraionForm, UserLoginForm, UserdataEditForm
from flask import request, render_template, redirect, Blueprint, flash, url_for
from flask_login import login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from . import db
from .models import user, post, img

page = Blueprint("page", __name__)


@page.route('/')
def hello_world():
    return render_template("homepage.html")


@page.before_request
def run():
    db.create_all()
    db.session.commit()


@page.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    form = PostUploadForm()
    if form.validate_on_submit():
        pic = form.img.data
        new_post = post(form.title.data, form.desc.data, form.ing.data, form.nutri.data, form.recipe.data, current_user.UID)
        db.session.add(new_post)
        db.session.commit()
        new_img = img(secure_filename(pic.filename),
                      base64.b64encode(pic.read()).decode('utf-8'),
                      mimetype=pic.mimetype,
                      PID=new_post.PID)
        db.session.add(new_img)
        db.session.commit()
        flash("Post Sumbitted Successfully","success")
        return redirect("/")
    else:
        return render_template("upload.html",form=form)


@page.route("/post/<Title>")
def display_post(Title):
    _post = post.query.filter_by(TITLE=Title).first()
    if _post:
        _img = img.query.filter_by(PID=_post.PID).first()
        return render_template("showpost.html", img=_img.bufferdata, mimetype=_img.mimetype, post=_post)
    else:
        return "No post with THat id", 404


@page.route("/del_post/<PID>", methods=["POST"])
def del_post(PID):
    del_post = post.query.filter_by(PID=PID,UID=current_user.UID).first()
    if del_post:
        post.query.filter_by(PID=PID).delete()
        img.query.filter_by(PID=PID).delete()
        db.session.commit()
        flash("Post Deleted Successfully","Success")
    else:
        flash("You are not the owner of that Post","error")
    return redirect("/account")


