FROM python:3.12

COPY . /jinx_erp_v2
WORKDIR /jinx_erp_v2

ENV DEBUG=False
ENV HOST=*
ENV DB_HOST=postgresql
ENV DB_PORT=5432
ENV DB_USER=admin
ENV DB_PASSWORD=admin@1996
ENV DB_NAME=jinx_erp_v2
ENV CELERY_BROKER_URL=amqp://admin:admin@1996@rabbitmq:5672//
ENV CHANNEL_BROKER_URL=redis://:admin@1996@redis:6379/0

RUN pip install --no-cache-dir -r requirements.txt
