FROM python:3.7

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
COPY Pipfile .
COPY Pipfile.lock .
COPY ./libs/ /libs

RUN pip install --upgrade pip && python -m pip install pipenv  
RUN pipenv install --system
RUN pipenv install /libs/drfdocs-0.0.12b0.tar.gz

RUN python manage.py collectstatic --noinput

# CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
CMD python manage.py runserver 0.0.0.0:8088

