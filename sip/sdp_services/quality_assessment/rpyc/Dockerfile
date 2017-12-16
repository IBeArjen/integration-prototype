#
# sdp_services/quality_assessment/rpyc/Dockerfile
#
FROM python:3.6-alpine3.6
LABEL maintainer="Benjamin Mort <ben.mort@gmail.com>"

# Copy python requirements file
COPY requirements.txt /app/requirements.txt

RUN apk update && \
    pip install -r /app/requirements.txt && \
    find /usr/local/lib/python3.6/ -name 'tests' -exec rm -r '{}' + && \
    rm -r /root/.cache

# RPyC service endpoint
EXPOSE 12345

# Working directory
WORKDIR /app

# Copy code to container working directory
COPY . /app/sip/qa

# Container healthcheck command
HEALTHCHECK --interval=10s --timeout=1s --start-period=5s --retries=3 \
    CMD python3 sip/qa/check_health.py localhost 12345 || exit 1

# Entrypoint (command that is run by default)
ENTRYPOINT ["python3", "-m", "sip.qa"]
