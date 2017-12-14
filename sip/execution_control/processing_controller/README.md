# Processing Controller Service

## Description

***NOTE: Detailed design of the Processing Controller is still required!
Please don't read too much into the description below!***

Handles resource provisioning and execution of scheduling and processing 
blocks. This service provides a high level interface for running SDP 
capabilities. In normal production, this service responds to commands 
issued from the `Master Controller`. The service is responsible for the 
allocation of Scheduling Blocks and Processing Blocks associated with a 
given SDP capability.

There are currently two implementations of this service based on the API
endpoint they expose:

- rpyc:  A processing controller with an RPyC interface
- tango: A processing controller with an Tango interface providing a set of 
         Tango Processing block devices

## Provided Interfaces

- Processing block interface
    - Tango devices or equivalent web service API
- Scheduling block interface
    - Tango devices or equivalent web service API

## Required Interfaces

- None


