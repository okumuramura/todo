from todo.todolist.models.task import Task


def test_task_init():
    task = Task('new task')

    assert task.title == 'new task'
