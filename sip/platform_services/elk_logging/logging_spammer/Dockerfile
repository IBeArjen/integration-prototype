FROM python:3.6.2-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"
RUN pip install python-logstash
WORKDIR /app
COPY __main__.py /app/logging_spammer/__main__.py
ENTRYPOINT ["python3", "-m", "logging_spammer"]
