from datetime import date
from http import HTTPStatus
from typing import Optional

import todo
from todo.todolist.models.task import Task


def test_add(fake_db):
    with todo.Session() as session:
        task_list = session.query(Task).all()

    assert len(task_list) == 0


def test_add_task(fake_db, client):
    response = client.post('/add', data={'title': 'new test task'})

    with todo.Session() as session:
        new_task: Optional[Task] = session.query(Task).first()

    assert response.status_code == HTTPStatus.FOUND
    assert new_task is not None
    assert new_task.title == 'new test task'


def test_update_invalid_task(fake_db, fake_tasks, client):
    data = {
        'title': 'new title'
    }
    response = client.post('/update/999', data=data)

    assert response.status_code == 404


def test_update_valid_task_without_date(fake_db, fake_tasks, client):
    data = {
        'title': 'new title #1',
        'description': 'this is test description'
    }
    response = client.post('/update/1', data=data)

    assert response.status_code == HTTPStatus.FOUND

    with todo.Session() as session:
        updated_task: Task = session.query(Task).filter(Task.id == 1).first()

    assert updated_task.title == data['title']
    assert updated_task.description == data['description']
    assert updated_task.date is None


def test_update_valid_task_with_date(fake_db, fake_tasks, client):
    data = {
        'title': 'new title #1',
        'date': '2022-03-14'
    }
    response = client.post('/update/1', data=data)

    assert response.status_code == HTTPStatus.FOUND

    with todo.Session() as session:
        updated_task: Task = session.query(Task).filter(Task.id == 1).first()

    assert updated_task.title == data['title']
    assert updated_task.description == ''
    assert updated_task.date == date(2022, 3, 14)


def test_existed_task_info(fake_db, fake_tasks, client):
    response = client.get('/1')

    assert response.status_code == HTTPStatus.OK


def test_invalid_task_info(fake_db, fake_tasks, client):
    response = client.get('/999')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_done_valid_task(fake_db, fake_tasks, client):
    response = client.get('/done/1')

    assert response.status_code == HTTPStatus.FOUND

    with todo.Session() as session:
        task = session.query(Task).filter(Task.id == 1).first()

    assert task.done is True

    response = client.get('/done/1')

    assert response.status_code == HTTPStatus.FOUND

    with todo.Session() as session:
        task = session.query(Task).filter(Task.id == 1).first()

    assert task.done is False


def test_done_invalid_task(fake_db, fake_tasks, client):
    response = client.get('/done/999')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_task(fake_db, fake_tasks, client):
    response = client.get('/delete/1')

    assert response.status_code == HTTPStatus.FOUND

    response = client.post('/delete/2')

    assert response.status_code == HTTPStatus.FOUND

    with todo.Session() as session:
        task1 = session.query(Task).filter(Task.id == 1).first()
        task2 = session.query(Task).filter(Task.id == 2).first()

    assert task1 is None
    assert task2 is None

    response = client.post('/delete/1')

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delte_invalid_task(fake_db, fake_tasks, client):
    response = client.post('/delete/999')

    assert response.status_code == HTTPStatus.NOT_FOUND
