import datetime
from pathlib import Path
from typing import Optional, Tuple

from flask import Blueprint, abort, redirect, render_template, request, url_for
from werkzeug import Response

import todo
from todo import logger
from todo.todolist.models.task import Task

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
    offset_str = request.args.get('offset', '')
    search_placeholder = ''

    try:
        offset = int(offset_str)
    except ValueError:
        offset = 0

    with todo.Session() as session:

        if search_query:
            search = f'%{search_query}%'
            search_placeholder = search_query

            elements_query = session.query(Task).filter(
                (Task.title.ilike(search)) | (Task.description.ilike(search))
            )

        else:
            elements_query = session.query(Task)

        total_elements = elements_query.count()
        tasks_list = elements_query.limit(5).offset(offset).all()
    pages = range((total_elements + 4) // 5)

    return (
        render_template(
            'todolist/task_list.html',
            list=tasks_list,
            search=search_placeholder,
            query=search_query,
            pages=pages,
            current_page=offset // 5,
        ),
        200,
    )


@todo_page.post('/add')
def add_task() -> Response:
    task_title = request.form.get('title')
    new_task = Task(task_title)

    with todo.Session() as session:
        session.add(new_task)
        session.commit()
        task_num = session.query(Task).count()

    logger.info(
        'user with ip %s added task \"%s\"', request.remote_addr, task_title
    )
    return redirect(
        url_for('.todo_list', offset=(task_num - 1) // 5 * 5), code=302
    )


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
        task: Optional[Task] = (
            session.query(Task).filter(Task.id == tid).first()
        )

        if task is not None:
            task.title = task_title
            task.description = task_description
            task.date = task_true_date

            session.commit()
            logger.info('task with id %d successfully updated', tid)
            return redirect(url_for('.todo_list'), code=302)
    logger.warning('task with id %d not exists!', tid)
    return abort(404)


@todo_page.route('/done/<int:tid>', methods=['GET', 'POST'])
def done_task(tid: int) -> Response:
    with todo.Session() as session:
        task: Optional[Task] = (
            session.query(Task).filter(Task.id == tid).first()
        )

        if task is not None:
            task.done = not task.done

            session.commit()
            logger.info(
                'task with id %d now has done status: %d', tid, int(task.done)
            )

            return redirect(url_for('.todo_list'), code=302)
    logger.warning('task with id %d not exists!', tid)
    return abort(404)


@todo_page.route('/delete/<int:tid>', methods=['GET', 'POST'])
def delete_task(tid: int) -> Response:
    with todo.Session() as session:
        task: Optional[Task] = (
            session.query(Task).filter(Task.id == tid).first()
        )

        if task is not None:
            task_num = session.query(Task).filter(Task.id < task.id).count()
            session.delete(task)
            session.commit()
            logger.info('task with id %d successfully deleted', tid)

            return redirect(
                url_for('.todo_list', offset=(task_num - 1) // 5 * 5), code=302
            )
    logger.warning('task with id %d not exists!', tid)
    return abort(404)


@todo_page.get('/<int:tid>')
def show_task(tid: int) -> str:
    with todo.Session() as session:
        task = session.query(Task).filter(Task.id == tid).first()
    if task is not None:
        return render_template('todolist/task_info.html', todo=task)
    logger.warning('task with id %d not exists!', tid)
    return abort(404)


@todo_page.errorhandler(404)
def task_not_found(_: Exception) -> Tuple[str, int]:
    return render_template('todolist/404_page.html'), 404
