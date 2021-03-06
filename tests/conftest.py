import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from todo import Base
from todo.__main__ import app as todo_app
from todo.todolist.models.task import Task


@pytest.fixture()
def app():
    todo_app.config.update({
        "TESTING": True,
    })
    yield todo_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def test_db():
    if os.path.exists('./test.db'):
        os.remove('./test.db')

    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(engine)
    TestSession = sessionmaker(engine)
    yield TestSession
    os.remove('./test.db')


@pytest.fixture()
def fake_db(mocker, test_db):
    mocker.patch('todo.Session', test_db)


@pytest.fixture()
def fake_tasks(test_db):
    tasks = [Task(f'test task #{i}') for i in range(5)]
    with test_db() as session:
        session.add_all(tasks)
        session.commit()


@pytest.fixture()
def fake_tasks_100(test_db):
    tasks = [Task(f'test task #{i}') for i in range(100)]
    with test_db() as session:
        session.add_all(tasks)
        session.commit()
