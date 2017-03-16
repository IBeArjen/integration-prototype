FROM ubuntu
MAINTAINER David Terrett
USER root

# Install Python 3 and pip
RUN apt-get -y update 
RUN apt-get -y install docker
RUN apt-get -y install python3 python3-pip
RUN apt-get -y install libboost-program-options-dev
RUN apt-get -y install libboost-system-dev
RUN apt-get -y install libboost-python-dev
RUN apt-get -y install python-numpy-dev
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
RUN apt-get -y install dnsutils

# Create non-privileged user
RUN adduser --disabled-password -gecos 'unprivileged user' sdp

# Set working directory
WORKDIR /home/sdp

# Copy the SIP
<<<<<<< HEAD
COPY common/ common/
COPY master/ master/
COPY slave/ slave/
COPY tasks/ tasks/
=======
>>>>>>> 672537f6980ded943e91a86a732cacc0475dcbbf
COPY sip/ sip/
