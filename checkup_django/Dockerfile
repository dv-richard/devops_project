FROM python:3.12

ARG http_proxy
ARG https_proxy
ARG no_proxy

ENV HTTP_PROXY=$http_proxy
ENV HTTPS_PROXY=$https_proxy
ENV NO_PROXY=$no_proxy

WORKDIR /app

# Pré-requis Debian
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    gcc \
    g++ \
    libpq-dev \
    libsqlite3-dev \
    nano \
    bash-completion


COPY requirements.txt .

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

RUN echo "source /etc/profile.d/bash_completion.sh" >> ~/.bashrc

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "mtpmetropole.asgi:application"]
