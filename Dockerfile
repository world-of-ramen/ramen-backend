FROM python:3.8.12-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app


RUN apt-get update && \
    apt-get install -y --no-install-recommends netcat && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./
RUN pip install --upgrade pip && pip install poetry && \
    poetry config virtualenvs.in-project true && \
    poetry install
    # poetry install --no-dev

COPY . ./

CMD poetry run alembic upgrade head && \
    poetry run uvicorn --host=0.0.0.0 app.main:app

# CMD poetry run uvicorn --host=0.0.0.0 app.main:app
