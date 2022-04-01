# ToDo List via Flask

## Description
Task manager (ToDo list) with web-interface.
### Features:
- Adding, executing and deleting tasks
- Search bar
- Pegination (5 tasks on page)
- Description and task time frame
- SQLite DB


## Install Requirements
```bash
pip install poetry
poetry install
```

## Start App
```bash
poetry shell
python -m todo start
# or
make start
```

## Make
```
help                           Show this help
test                           Runs pytest
lint                           Lint code
format                         Formats all files
start                          Start app
ci                             Lint code then run tests
```

## License
The MIT License (MIT)