FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings

WORKDIR /opt/src

COPY pyproject.toml pyproject.toml
RUN mkdir -p /opt/src/static/ && \
    mkdir -p /opt/src/media/ && \
    pip install --upgrade pip && \
    pip install 'poetry>=1.4.2' && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-dev

COPY . .

ARG APP_SCRIPT
COPY ./${APP_SCRIPT} /app_script.sh
RUN chmod +x /app_script.sh
ENTRYPOINT ["/app_script.sh"]
