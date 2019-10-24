# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3.6

# If you prefer miniconda:
#FROM continuumio/miniconda3

LABEL Name=perdana_indonesia_app Version=1.0.0

WORKDIR /web
ADD . /web

# Using pip:
# RUN python3 -m pip install -r requirements.txt
# CMD ["python3", "-m", "perdana_indonesia_app"]

# Using pipenv:
COPY Pipfile /web
COPY Pipfile.lock /web

RUN python -m pip install pipenv
RUN pipenv install --system --dev

EXPOSE 8088

CMD ["python", "manage.py", "runserver", "0.0.0.0:8088"]

# Using miniconda (make sure to replace 'myenv' w/ your environment name):
#RUN conda env create -f environment.yml
#CMD /bin/bash -c "source activate myenv && python3 -m perdana_indonesia_app"
