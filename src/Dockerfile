FROM python:3.11-slim

WORKDIR /opt/todolist

ENV PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    PYTHON_PATH=/opt/todolist

# ENV POSTGRES_HOST=postgres

RUN groupadd --system service && \
    useradd --system -g service api

RUN apt update && apt install build-essential libpq-dev -y

RUN pip install --upgrade pip && \
    pip install "poetry==1.5.*"
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false && \
    poetry install --without dev --no-ansi --no-interaction --no-root

COPY src/ ./

# дальше действия от пользователя
USER api

ENTRYPOINT ["bash", "entrypoint.sh"]

# CMD ["./manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "todolist/wsgi", "-w", "2", "-b", "0.0.0.0:8000"]

# документирование для 'docker inspect'
EXPOSE 8000
