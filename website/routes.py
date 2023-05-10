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


@page.route("/login", methods=["POST", "GET"])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        login_user(form.user, remember=True)
        return redirect("/")
    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0],"error")
    return render_template("login.html",form=form)


@page.route("/register", methods=["POST", "GET"])
def register():
    form = UserRegistraionForm()
    if form.validate_on_submit():
        new_user = user(form.username.data,
         generate_password_hash(form.password2.data, method="sha256"),
          form.email.data)
        db.session.add(new_user)
        db.session.commit()
        flash("User Successfully Created","success")
        return redirect("/login")
    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0],"error")
        return redirect(url_for("page.register"))
    return render_template("register.html", form=form)


@login_required
@page.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@page.route("/post/<Title>")
def display_post(Title):
    _post = post.query.filter_by(TITLE=Title).first()
    if _post:
        _img = img.query.filter_by(PID=_post.PID).first()
        return render_template("showpost.html", img=_img.bufferdata, mimetype=_img.mimetype, post=_post)
    else:
        return "No post with THat id", 404

@login_required
@page.route("/account")
def user_profile():
    return render_template("account.html",user=current_user)


@page.route("/profile/<username>")
def  view_profile(username):
    if current_user.USERNAME == username:
        return redirect("/account")
    User = user.query.filter_by(USERNAME=username).first()
    if User:
        return render_template("user_posts.html",user=User)
    flash("No such User found","error")
    return render_template("/")

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

@login_required(func)
@page.route("/profile/edit",methods=["GET","POST"])
def edit_profile():
    form = UserdataEditForm(user=current_user)
    if form.validate_on_submit():
        current_user.USERNAME = form.username.data
        current_user.EMAIL = form.email.data
        Logout = False
        print(form.password2.data)
        if form.password2.data != "":
            current_user.PASSWORD = generate_password_hash(form.password2.data)
            Logout = True
        db.session.commit()
        flash("Profile Updated Successfully", "success")
        if Logout:
            return redirect("/logout")
        return redirect("/profile/edit")
    if form.errors != {}:
        for error in form.errors.values():
            flash(error[0],"error")
    return render_template("editProfile.html",form=form)
