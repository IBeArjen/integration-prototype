# A Note on where data is stored within SIP


***Question: Where in SIP to we store data?***

- **Container orchestration runtime** (eg Docker engine in swarm mode with 
    overlay network)
  - Provides a list of services that are running (with health)
  - Provides service discovery (with overlay network)
  - Services configured using a docker-stack file.
  - interaction via a `sip/platform_services` interface?

- **Configuration Db** (in `sip/platform_services`)
  - Static configuration for used to configure services

- **(Science) Data model** (in `sip/sdp_services`)
  - ...

- **EF Runtime**

- **Data buffers**

- **Data queues**

- **Command / event queues**

- **Alarms**


## Notes:

<http://microservices.io/patterns/data/database-per-service.html>

- Most services will need to persist data in some way.
- Services much be loosely coupled so they can be developed, deployed and 
  scaled independently.
- Some business transactions must enforce invariants that span multiple 
  services.
- Some business transactions need to query data owned in multiple services.
- Databases must be replicated and sharded in order to scale.
- Different services have different storage requirements (eg. SQL vs NoSQL)

- Have a database per service (not per service replica!)
 


<https://www.confluent.io/blog/apache-kafka-for-service-architectures/>
