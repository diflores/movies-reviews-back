# Movie Reviews Back

## About

Back-end for our Movies Reviews app.

## How to run

1. Install Poetry:

```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

2. Install requirements with: `poetry install`.
3. Make sure you have defined the following environment variables:

```
SECRET_KEY
DATABASE_USER
DATABASE_PASSWORD
DATABASE_HOST
DATABASE_PORT
DATABASE_NAME
MOVIE_DATABASE_API_KEY
MOVIE_DATABASE_BASE_URL
```
4. Run with `poetry run uvicorn app.main:app --reload`.
5. See live documentation at http://127.0.0.1:8000/docs/.
