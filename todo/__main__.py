from typer import Typer

from todo import Base, app, engine
from todo.todolist.todolist import todo_page

args = Typer()

app.register_blueprint(todo_page, url_prefix='/')


@args.command(name='init')
def init_db() -> None:
    Base.metadata.create_all(engine)


@args.command()
def start() -> None:
    app.run()


if __name__ == '__main__':
    args()
