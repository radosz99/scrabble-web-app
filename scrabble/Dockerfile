FROM python:3.7.7-alpine

ENV FLASK_APP "game/hello.py"

RUN apk update
RUN pip install --no-cache-dir pipenv

WORKDIR /usr/src/app

COPY Pipfile Pipfile.lock ./
COPY game ./game
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]