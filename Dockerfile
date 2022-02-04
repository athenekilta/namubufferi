# syntax=docker/dockerfile:1
FROM node:16
WORKDIR /tmp/reactapp/
COPY reactapp/package.json reactapp/yarn.lock ./
RUN yarn install
COPY reactapp/public/ ./public/
COPY reactapp/src/ ./src/
RUN yarn build

FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt update && apt install -y \
    libpq-dev \
    python3-dev \
    && python3 -m pip install --upgrade \
    pip \
    pipenv \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /srv/namubufferi/
COPY Pipfile* ./
# Heroku uses a non-root user
# https://pipenv.pypa.io/en/latest/advanced/#custom-virtual-environment-location
ENV WORKON_HOME=/usr/local/share/virtualenvs/
ENV PIPENV_DONT_LOAD_ENV=1
RUN pipenv install --deploy
COPY . ./
COPY --from=0 /tmp/reactapp/static/ ./reactapp/static/
ENTRYPOINT ["./docker-entrypoint.sh"]
# Will bind to 0.0.0.0:$PORT
# https://docs.gunicorn.org/en/stable/settings.html#server-socket
CMD ["gunicorn", "namubufferi.wsgi"]
