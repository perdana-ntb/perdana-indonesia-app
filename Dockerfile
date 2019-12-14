FROM python:3.7

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
COPY Pipfile .
COPY Pipfile.lock .

RUN pip install --upgrade pip && python -m pip install pipenv  
RUN pipenv install --system

RUN python manage.py collectstatic --noinput

CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

