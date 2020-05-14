FROM python:3.7-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk --no-cache add python3 \
    build-base \
    python3-dev \
    # wget dependency
    openssl \
    # dev dependencies
    git \
    bash \
    sudo \
    py3-pip \
    libc-dev \
    linux-headers \
    mariadb-dev \
    # Pillow dependencies
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev \
    gcc

COPY . .
COPY Pipfile .
COPY Pipfile.lock .
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

RUN pip install --upgrade pip --no-cache-dir && python -m pip install pipenv --no-cache-dir
RUN pipenv install --system

EXPOSE 8000
ENTRYPOINT ["/docker-entrypoint.sh"]