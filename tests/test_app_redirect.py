from http import HTTPStatus


def test_add_redirect(fake_db, fake_tasks, client):
    task_data = {
        'title': 'new test'
    }
    response = client.post('/add', data=task_data, follow_redirects=True)

    assert response.status_code == HTTPStatus.OK
    assert len(response.history) == 1
    assert response.request.path == '/'
    assert response.request.args.get('offset') == '5'


def test_delete_redirect(fake_db, fake_tasks, client):
    response = client.post('/delete/3', follow_redirects=True)

    assert response.status_code == HTTPStatus.OK
    assert len(response.history) == 1
    assert response.request.path == '/'
    assert response.request.args.get('offset') == '0'
