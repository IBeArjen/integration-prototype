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


 
