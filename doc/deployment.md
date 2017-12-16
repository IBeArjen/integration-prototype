# SIP Deployment

## Introduction

In deployment the SIP code falls into two categories:

- **Services**: Small, independently deployable applications which provide 
  a 'service' or set of functions to other parts of the SIP code.
  Where possible, services are to be run using container orchestration to 
  provide a reliable, horizontally scalable system. 
  Services will communicate using standard protocols such as HTTP and will 
  adhere to a set of contractually specified interfaces defined by the readme
  file found in the package folder where the service code resides.
  Wherever possible, services will be stateless and should always be easy to 
  replace. Services will be deployed as a software stack, and once deployed, 
  will be self managing and always available without user intervention or 
  catastrophic hardware failure.

- **Capabilities**: Are the set of Pipeline Workflows *(see above)*
  or specialised applications that can be run by the system at a given time.

## Deployment with Docker

### Using single Docker engine

Build the SIP Docker images with:

```bash
docker-compose build
```

Run the SIP Master Controller (RPyC flavour) container:

```bash
docker run --rm -d -p12345:12345 skasip/master_rpyc
```

This can be tested with an experimental CLI script interfacing with the RPyC
endpoints. This can be found in 
`sip/execution_control/master_controller/rpyc/cli/`
and can be run with the following command:

```bash
python3 sip/execution_control/master_controller/rpyc/cli/sip_master_cli.py
```

For arguments and options run the script with no arguments or use the `-h`
flag.


All SIP Docker services can be started with the single command: 

```bash
docker-compose up -d
```

All running SIP services can be then stopped with the single command:

```bash
docker-compose stop
```

or 

```bash
docker-compose kill
```

All finished SIP service containers can then be removed with the command:

```bash
docker-compose rm [-f]
```

### Docker Swarm mode

***TODO(BM)***

### Useful docker commands

To view logs from a running container:

```bash
docker logs [-f] CONATINER
```

To clean up dangling images:

```bash
docker image prune -f
```


