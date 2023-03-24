from flask import (
    Blueprint,
    render_template,
    request,
    g,
    redirect,
    url_for,
    flash
)
from dec import login_required
from .forms import TodolistForm
from models import TodolistModel
from exts import db
from sqlalchemy import or_

bp = Blueprint("todo", __name__, url_prefix="/")


# index surface, get todolists from the model and order them
@bp.route("/")
def index():
    todolists = TodolistModel.query.order_by(db.text("module")).order_by(db.text("deadline")).all()
    return render_template("index.html", todolists=todolists)


# the page for restoring the status of the list
# change the status by clicking function and commit to the database
@bp.route("/<web>/<int:todolist_id>")
def reform_status(web, todolist_id):
    todolist = TodolistModel.query.filter_by(id=todolist_id).first()
    if todolist.status == "Completed":
        todolist.status = "Uncompleted"
    else:
        todolist.status = "Completed"
    db.session.commit()

    # different page have different redirect, refer to the <web>
    if web == "index":
        return redirect('/')
    else:
        return redirect('/%s' % web)


# the page for restoring the importance of the list
# change teh importance by clicking function and commit to the database
@bp.route("/<web>/change_imp/<int:todolist_id>")
def reform_imp(web, todolist_id):
    todolist = TodolistModel.query.filter_by(id=todolist_id).first()
    if todolist.importance == "important":
        todolist.importance = "none"
    else:
        todolist.importance = "important"
    db.session.commit()

    # different page have different redirect, refer to the <web>
    if web == "index":
        return redirect('/')
    else:
        return redirect('/%s' % web)


# get the module title as a variable and direct the web to different page
@bp.route("/category/<string:todolist_module>")
def category(todolist_module):
    todolists = TodolistModel.query.order_by(db.text("module")).order_by(db.text("deadline")).all()
    # send the todolists and todolist_module as two variables to the main web
    return render_template("category.html", todolists=todolists, todolist_module=todolist_module)


# get the important list and store them in the important_todolists
@bp.route("/important")
def important():
    important_todolists = TodolistModel.query.order_by(db.text("module")).order_by(db.text("deadline")).all()
    return render_template("important_todo.html", todolists=important_todolists)


# get the completed list and store them in the completed_todolists
@bp.route("/completed")
def completed():
    completed_todolists = TodolistModel.query.order_by(db.text("module")).order_by(db.text("deadline")).all()
    return render_template("completed_todo.html", todolists=completed_todolists)


# get the uncompleted list and store them in the uncompleted_todolists
@bp.route("/uncompleted")
def uncompleted():
    uncompleted_todolists = TodolistModel.query.order_by(db.text("module")).order_by(db.text("deadline")).all()
    return render_template("uncompleted_todo.html", todolists=uncompleted_todolists)


# add todolist, must log in
# get the input and store
@bp.route("/todolist/public", methods=['GET', 'POST'])
@login_required
def add_newtodo():
    # whether the user have logged, if not, jump to login page
    if request.method == 'GET':
        return render_template("add_newTodo.html")
    else:
        form = TodolistForm(request.form)
        if form.validate():
            assessment_title = form.assessment_title.data
            module = form.module.data
            deadline = form.deadline.data
            importance = form.importance.data
            status = form.status.data
            description = form.description.data
            # store the data and update to the database
            todolist = TodolistModel(assessment_title=assessment_title, module=module, deadline=deadline,
                                     importance=importance, status=status, description=description, author=g.user)
            db.session.add(todolist)
            db.session.commit()
            return redirect("/")
        else:
            flash("Wrong format for the input!")
            return redirect(url_for("todo.add_newtodo"))


# delete the chosen todolist according to the id
# update the change in the database
@bp.route("/todolist/delete/<int:todolist_id>")
def delete_todo(todolist_id):
    list = TodolistModel.query.get(todolist_id)
    if not list:
        flash("Nothing related found to deleted!")
    else:
        try:
            db.session.delete(list)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
    return redirect("/")


# edit the chosen todolist according to the id
# update the change in the database
@bp.route("/todolist/edit/<int:todolist_id>", methods=['GET', 'POST'])
@login_required
def edit_todo(todolist_id):
    # whether the user have logged, if not, jump to login page
    if request.method == 'GET':
        todolist = TodolistModel.query.get(todolist_id)
        return render_template("edit.html", todolist=todolist)
    else:
        todolist = TodolistModel.query.get(todolist_id)
        form = TodolistForm(request.form)
        if form.validate():
            todolist.assessment_title = form.assessment_title.data
            todolist.module = form.module.data
            todolist.deadline = form.deadline.data
            todolist.importance = form.importance.data
            todolist.status = form.status.data
            todolist.description = form.description.data
            db.session.commit()
            return redirect("/")
        else:
            flash("Wrong format for the input!")
            return redirect(url_for('todo.edit_todo', todolist_id=todolist.id))


# choose the specific todolist according to the id
# order by the deadline time
@bp.route("/todolist/<int:todolist_id>")
def todolist_detail(todolist_id):
    todolists = TodolistModel.query.order_by(db.text("deadline")).all()
    return render_template("detail.html", todolists=todolists, todolist_id=todolist_id)


# search method use for search the key word
# title, description, module contains key word
@bp.route("/todolist/search")
def search():
    # /search?q=element you are searching for
    s = request.args.get("search")
    todolists = TodolistModel.query.filter(or_(TodolistModel.assessment_title.contains(s),
                                               TodolistModel.description.contains(s),
                                               TodolistModel.module.contains(s))).order_by(db.text("deadline"))
    return render_template("index.html", todolists=todolists)
