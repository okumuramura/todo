from http import HTTPStatus


def test_task_list(fake_db, client, fake_tasks):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK


def test_task_list_with_search(fake_db, fake_tasks, client):
    response = client.get('/?q=1')
    assert response.status_code == HTTPStatus.OK
