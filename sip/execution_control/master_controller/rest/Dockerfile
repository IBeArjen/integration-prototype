#
# master_controller/rest/Dockerfile
#
FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

# Copy python requirements file
COPY requirements.txt /app/requirements.txt

RUN apk update && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    apk add --no-cache curl && \
    find /usr/local/lib/python3.6/ -name 'tests' -exec rm -r '{}' + && \
    rm -r /root/.cache

# REST endpoint
EXPOSE 5555

# Working directory
WORKDIR /app

# Copy code to container working directory
COPY . /app/sip/master

# Container healthcheck command
HEALTHCHECK --interval=15s --timeout=2s --start-period=5s --retries=2 \
    CMD curl -f http://localhost:5555/healthcheck || exit 1

# Entrypoint (command that is run by default)
ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:5555", "sip.master.app:APP"]

