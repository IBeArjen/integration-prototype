# Master Controller (REST flavour)

## Purpose

This implementation of SIP master controller emulates the SDP-TM command
interface with REST.

It implements the "Master Controller" component of the SDP architecture.

## Responsibilities

- Provides the SDP control interface to TM.
- Implements the TM mandated states.
- Monitors the SDP service tasks and changes state as appropriate.
- Forwards processing block device creation command to the processing block
 controller.

## Provided interfaces


## Required interfaces


## Dependencies


## References

- <http://flask.pocoo.org/>
- <https://flask-restful.readthedocs.io/en/latest/index.html>
- <http://gunicorn.org/>
    - <http://gunicorn.org/#deployment>
- <http://nginx.org>
    - <https://www.nginx.com/blog/introduction-to-microservices/>
- <https://content.pivotal.io/blog/understanding-when-to-use-rabbitmq-or-apache-kafka>
