FROM docker.elastic.co/kibana/kibana:5.6.1
RUN kibana-plugin install \
    https://github.com/sivasamyk/logtrail/releases/download/v0.1.21/logtrail-5.6.1-0.1.21.zip
COPY logtrail.json /usr/share/kibana/plugins/logtrail/logtrail.json
