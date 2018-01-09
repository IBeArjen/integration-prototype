# Queues in SIP

## RabbitMQ vs Kafka

<https://content.pivotal.io/blog/understanding-when-to-use-rabbitmq-or-apache-kafka>

### RabbitMQ

- Traditional message broker that implements a variety of protocols
- General purpose message broker, employing several variations of 
  point-to-point, request/reply and pub-sub.
- Uses a **smart broker / dumb consumer** model.
    - Broker keeps track of the consumer state.
- Communication is synchronous or asynchronous as needed. 
- Publishers send messages to exchanges and consumers retrieve messages from 
  queues. 
- Decoupling producers from queues via exchanges ensures that producers are 
  not burdened with hardcoded routing decisions.
- Number of distributed deployment scenarios.


### Kafka

- High volume pub-sub designed to be durable, fast and scalable.
- Is is essence a durable message store, similar to a log, run in a server
  cluster, that  stores streams of records in categories called topics.
- Messages consist of a key, value and timestamp.
- **dump broker / smart consumer** model 
- Requires Zookeeper to run.

## Use cases

- Connecting services together
- Supporting logging
- Sending (and storing) data (eg. calibration solutions)



