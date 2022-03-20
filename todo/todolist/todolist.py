import datetime
from pathlib import Path
from typing import Optional, Tuple

from flask import Blueprint, abort, redirect, render_template, request, url_for
from werkzeug import Response

import todo
from todo.todolist.models.task import Task
from todo import logger


todo_page = Blueprint(
    'todo',
    __name__,
    static_folder=Path('./static'),
    template_folder='./templates',
    static_url_path='todo/static',
)


@todo_page.get('/')
def todo_list() -> Tuple[str, int]:
    search_query = request.args.get('q')
    search_placeholder = ''

    if search_query:
        search = f'%{search_query}%'
        search_placeholder = search_query

        with todo.Session() as session:
            tasks_list = session.query(Task).filter(
                (Task.title.like(search)) | (Task.description.like(search))).all()

    else:
        with todo.Session() as session:
            tasks_list = session.query(Task).all()
    return render_template('todolist/task_list.html', list=tasks_list, search=search_placeholder), 200


@todo_page.post('/add')
def add_task() -> Response:
    task_title = request.form.get('title')
    new_task = Task(task_title)
    with todo.Session() as session:
        session.add(new_task)
        session.commit()
    logger.info(f'user with ip {request.remote_addr} added task \"{task_title}\"')
    return redirect(url_for('.todo_list'), code=302)


@todo_page.post('/update/<int:tid>')
def update_task(tid: int) -> Response:
    task_title = request.form.get('title')
    task_description = request.form.get('description', '')
    task_date = request.form.get('date', '')

    try:
        task_true_date = datetime.date.fromisoformat(task_date)
    except ValueError:
        task_true_date = None

    with todo.Session() as session:
        task: Optional[Task] = session.query(Task).filter(Task.id == tid).first()

        if task is not None:
            task.title = task_title
            task.description = task_description
            task.date = task_true_date

            session.commit()
            logger.info(f'task with id {tid} successfully updated')
            return redirect(url_for('.todo_list'), code=302)
    logger.warning(f'task with id {tid} not exists!')
    return abort(404)


@todo_page.get('/<int:tid>')
def show_task(tid: int) -> str:
    with todo.Session() as session:
        task = session.query(Task).filter(Task.id == tid).first()
    if task is not None:
        return render_template('todolist/task_info.html', todo=task)
    logger.warning(f'task with id {tid} not exists!')
    return abort(404)


@todo_page.errorhandler(404)
def task_not_found(_: Exception) -> Tuple[str, int]:
    return render_template('todolist/404_page.html'), 404
