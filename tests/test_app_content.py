from lxml import html


def test_todo_list(fake_db, fake_tasks, client):
    response = client.get('/')
    page = html.fromstring(response.data.decode('utf-8'))

    assert page.xpath('//div[@class="header"]/a/text()')[0] == 'TODO LIST'
    assert len(page.xpath('//div[@class="pager"]/*')) == 0  # one page
    assert len(page.xpath('//div[@class="content"]/*')) == 5  # 5 tasks

    first_task = page.xpath('//div[@class="content"]/*')[0]

    assert first_task.xpath('./a[@class="tasktitle"]/text()')[0] == 'test task #0'
    assert first_task.xpath('./a[@class="tasktitle"]/@href')[0] == '/1'


def test_todo_list_with_query(fake_db, fake_tasks, client):
    response = client.get('/?q=3')
    page = html.fromstring(response.data.decode('utf-8'))

    assert len(page.xpath('//div[@class="pager"]/*')) == 0  # one page
    assert len(page.xpath('//div[@class="content"]/*')) == 1  # 1 task

    first_task = page.xpath('//div[@class="content"]/*')[0]

    assert first_task.xpath('./a[@class="tasktitle"]/text()')[0] == 'test task #3'
    assert first_task.xpath('./a[@class="tasktitle"]/@href')[0] == '/4'


def test_todo_list_paging(fake_db, fake_tasks_100, client):
    response = client.get('/')
    page = html.fromstring(response.data.decode('utf-8'))

    assert len(page.xpath('//div[@class="pager"]/*')) == 20  # 20 pages
    assert len(page.xpath('//div[@class="content"]/*')) == 5  # 5 tasks


def test_todo_info(fake_db, fake_tasks, client):
    response = client.get('/1')
    page = html.fromstring(response.data.decode('utf-8'))

    assert page.xpath('//div[@class="content"]/form/input/@value') == ['test task #0', '', 'None', 'Применить']
