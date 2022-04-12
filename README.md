# World of Ramen
World of Ramen Backend System
## install python
- Install python3.9 (Example: https://www.python.org/downloads/macos/)
- Install python3.8 (Example: https://stringpiggy.hpd.io/mac-osx-python3-multiple-pyenv-install/)
- Install python3.6 (Example: https://stdworkflow.com/433/macos-installs-multiple-versions-of-python)
- If pyenv doesn't work, you should run the command below and `source` it:
```
echo 'eval "$(pyenv init --path)"' >> ~/.zprofile
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

## venv
- `use python3.9`
- `python3.9 -m venv venv`
- `. venv/bin/activate`
- `python -V (check python version)`
- `pip install --upgrade pip`
- `pip install poetry`
- `please check poetry's path to make sure it's from python3.9: run *which poetry*`
- `the correct venv's poetry path would like: /Users/kangchih/world-of-ramen/ramen-backend/venv/bin/poetry`
- `if not, deactivate the venv and enter again: run *deactivate*`
- `poetry install`

- `use pyenv`
- `pyenv shell 3.9.2`
- `pyenv init`
- `eval "$(pyenv init -)"`
- `python -m venv venv`
- `. venv/bin/activate`
- `pip install --upgrade pip`
- `please check poetry's path to make sure it's from python3.9: run *which poetry*`
- `the correct venv's poetry path would like: /Users/kangchih/world-of-ramen/ramen-backend/venv/bin/poetry`
- `if not, deactivate the venv and enter again: run *deactivate*`
- `pip install poetry`
- `poetry install`

## run service
- `uvicorn app.main:app --reload`

## swagger document
- `http://localhost:8000/docs`

## pre-commit installation
- reference `https://pre-commit.com/`
- `pip3 install pre-commit`
- `pre-commit install`

## pre-commit run
- Run this command `pre-commit run --verbose --all-files`
## db schema
- Run this command `alembic upgrade head` if table hasn't yet created
- Note that if you run `alembic upgrade head` with error `ModuleNotFoundError: No module named 'app'` try `PYTHONPATH=. alembic upgrade head`
- ImportError issue: `https://stackoverflow.com/questions/33821470/importing-app-when-using-alembic-raises-importerror`
- update schema EX: `alembic revision -m "create xxx table"`
- downgrade schema EX: `PYTHONPATH=. alembic downgrade -1`
## alembic example
- reference: `https://alembic.sqlalchemy.org/en/latest/tutorial.html#`
- migration: `https://alembic.sqlalchemy.org/en/latest/tutorial.html#create-a-migration-script`

## db example sql
select currval('plan_attachments_id_seq')
select setval('plan_attachments_id_seq', (select max(id) from plan_attachments)+1)
select currval('notifications_id_seq')
select setval('notifications_id_seq', (select max(id) from notifications)+1)
select currval('plan_pictures_id_seq')
select setval('plan_pictures_id_seq', (select max(id) from plan_pictures)+1)
select currval('plans_id_seq')
select setval('plans_id_seq', (select max(id) from plans)+1)
select currval('users_id_seq')
select setval('users_id_seq', (select max(id) from users)+1)
select currval('commentaries_id_seq')
select setval('commentaries_id_seq', (select max(id) from commentaries)+1)

## Run db
- `export POSTGRES_DB=ramen POSTGRES_PORT=5432 POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres`
- `docker run --name pgdb --rm -e POSTGRES_USER="$POSTGRES_USER" -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" -e POSTGRES_DB="$POSTGRES_DB" postgres -p 5432:5432`
- `export POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pgdb) createdb --host=$POSTGRES_HOST --port=$POSTGRES_PORT --username=$POSTGRES_USER $POSTGRES_DB`

# original
Quickstart
----------

First, run ``PostgreSQL``, set environment variables and create database. For example using ``docker``: ::

    export POSTGRES_DB=ramen POSTGRES_PORT=5432 POSTGRES_USER=postgres POSTGRES_PASSWORD=postgres
    docker run --name pgdb --rm -e POSTGRES_USER="$POSTGRES_USER" -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" -e POSTGRES_DB="$POSTGRES_DB" postgres
    export POSTGRES_HOST=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' pgdb)
    createdb --host=$POSTGRES_HOST --port=$POSTGRES_PORT --username=$POSTGRES_USER $POSTGRES_DB

Then run the following commands to bootstrap your environment with ``poetry``: ::

    git clone https://github.com/nsidnev/fastapi-realworld-example-app
    cd fastapi-realworld-example-app
    poetry install
    poetry shell

Then create ``.env`` file (or rename and modify ``.env.example``) in project root and set environment variables for application: ::

    touch .env
    echo APP_ENV=dev
    echo DATABASE_URL=postgresql://$POSTGRES_USER:$POSTGRES_PASSWORD@$POSTGRES_HOST:$POSTGRES_PORT/$POSTGRES_DB >> .env
    echo SECRET_KEY=$(openssl rand -hex 32) >> .env
    echo BUCKET_NAME=world-of-ramen >> .env

To run the web application in debug use::

    alembic upgrade head
    uvicorn app.main:app --reload

Run tests
---------

Tests for this project are defined in the ``tests/`` folder.

This project uses `pytest
<https://docs.pytest.org/>`_ to define tests because it allows you to use the ``assert`` keyword with good formatting for failed assertations.


To run all the tests of a project, simply run the ``pytest`` command: ::

    $ pytest
    ================================================= test session starts ==================================================
    platform linux -- Python 3.8.3, pytest-5.4.2, py-1.8.1, pluggy-0.13.1
    rootdir: /home/some-user/user-projects/fastapi-realworld-example-app, inifile: setup.cfg, testpaths: tests
    plugins: env-0.6.2, cov-2.9.0, asyncio-0.12.0
    collected 90 items

    tests/test_api/test_errors/test_422_error.py .                                                                   [  1%]
    tests/test_api/test_errors/test_error.py .                                                                       [  2%]
    tests/test_api/test_routes/test_articles.py .................................                                    [ 38%]
    tests/test_api/test_routes/test_authentication.py ..                                                             [ 41%]
    tests/test_api/test_routes/test_comments.py ....                                                                 [ 45%]
    tests/test_api/test_routes/test_login.py ...                                                                     [ 48%]
    tests/test_api/test_routes/test_profiles.py ............                                                         [ 62%]
    tests/test_api/test_routes/test_registration.py ...                                                              [ 65%]
    tests/test_api/test_routes/test_tags.py ..                                                                       [ 67%]
    tests/test_api/test_routes/test_users.py ....................                                                    [ 90%]
    tests/test_db/test_queries/test_tables.py ...                                                                    [ 93%]
    tests/test_schemas/test_rw_model.py .                                                                            [ 94%]
    tests/test_services/test_jwt.py .....                                                                            [100%]

    ============================================ 90 passed in 70.50s (0:01:10) =============================================
    $

This project does not use your local ``PostgreSQL`` by default, but creates it in ``docker`` as a container (you can see it if you type ``docker ps`` when the tests are executed, the docker container for ``PostgreSQL`` should be launched with with a name like ``test-postgres-725b4bd4-04f5-4c59-9870-af747d3b182f``). But there are cases when you don't want to use ``docker`` for tests as a database provider (which takes an additional +- 5-10 seconds for its bootstrap before executing the tests), for example, in CI, or if you have problems with the ``docker`` driver or for any other reason. In this case, you can run the tests using your already running database with the following command: ::

   $ USE_LOCAL_DB_FOR_TEST=True pytest

Which will use your local database with DSN from the environment variable ``DATABASE_URL``.


If you want to run a specific test, you can do this with `this
<https://docs.pytest.org/en/latest/usage.html#specifying-tests-selecting-tests>`_ pytest feature: ::

    $ pytest tests/test_api/test_routes/test_users.py::test_user_can_not_take_already_used_credentials

Deployment with Docker
----------------------

You must have ``docker`` and ``docker-compose`` tools installed to work with material in this section.
First, create ``.env`` file like in `Quickstart` section or modify ``.env.example``.
``POSTGRES_HOST`` must be specified as `db` or modified in ``docker-compose.yml`` also.
Then just run::

    docker-compose up -d db
    docker-compose up -d app

Application will be available on ``localhost`` in your browser.

Web routes
----------

All routes are available on ``/docs`` or ``/redoc`` paths with Swagger or ReDoc.


Project structure
-----------------

Files related to application are in the ``app`` or ``tests`` directories.
Application parts are:

::

    app
    ├── api              - web related stuff.
    │   ├── dependencies - dependencies for routes definition.
    │   ├── errors       - definition of error handlers.
    │   └── routes       - web routes.
    ├── core             - application configuration, startup events, logging.
    ├── db               - db related stuff.
    │   ├── migrations   - manually written alembic migrations.
    │   └── repositories - all crud stuff.
    ├── models           - pydantic models for this application.
    │   ├── domain       - main models that are used almost everywhere.
    │   └── schemas      - schemas for using in web routes.
    ├── resources        - strings that are used in web responses.
    ├── services         - logic that is not just crud related.
    └── main.py          - FastAPI application creation and configuration.


Example
-------

Create a store:

::
curl -X 'POST' \
  'http://localhost:8000/api/store' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "store": {
    "name": "麵屋吉光",
    "phone": "0912345678",
    "address": "300新竹市東區關新東路138號1樓",
    "rating": 4.5,
    "place_id": "ChIJ9UlJNeA3aDQRQUVwgiMJhm8",
    "review_count": 100,
    "image": {
      "style": "cover",
      "url": "https://lh5.googleusercontent.com/p/AF1QipN6j0ksXQ0jmPcvbgvRSHE8SBYu9tmMs6xlVw0I=w408-h305-k-no",
      "width": "400",
      "height": "400",
      "contentType": "image/png"
    },
    "social_media": {
      "facebook": "https://www.facebook.com/ramenkikkou"
    },
    "business_hours": {
      "mo": "星期一 17:00–21:00",
      "tu": "星期二 17:00–21:00",
      "we": "星期三 17:00–21:00",
      "th": "星期四 17:00–21:00",
      "fr": "星期五 17:00–21:00",
      "sa": "休息",
      "su": "星期日 17:00–21:00"
    },
    "location": {
      "lat": 24.7837158,
      "lng": 121.0197911
    },
    "status": 1
  }
}'

Create an user:

::
curl -X 'POST' \
  'http://localhost:8000/api/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "user": {
    "wallet_address": "0x1234567890",
    "image": "https://cdn0.techbang.com/system/excerpt_images/93045/post_inpage/ad5d7ded784b3c54562d4ee73d89dd79.jpg?1640747883"
  }
}'
