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

CMD gunicorn config.wsgi_heroku:application --bind 0.0.0.0:$PORT
# CMD python manage.py runserver 0.0.0.0:8088

