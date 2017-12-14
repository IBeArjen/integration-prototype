# Execution Framework Interface

## Description

This package contains a library which provides a common interface to 
execution frameworks (essentially an adapter pattern). This library is used 
by the Processing Controller Service to run Science Pipeline workflows 
without having to know about the details of the particular Execution Framework 
implementation being run against. 

***Note: This library could, and probably should, be developed elsewhere.
ie. the abstract interface could be defined by the Processing Controller
and the given Execution Framework specialisation could be in the 
`exection_frameworks` package.<br>
It is included in SIP as a separate package to be consistent with the 
SDP architecture.*** 

# Provided Interface

High level library API used to run applications using an Execution Framework
runtime without having to know anything about the implementation of the 
execution framework or its runtime.
 
Methods provided:

- start()
- stop()
- status()  

# Required Interface

- Implantation of the abstract interface will need a instance of their 
  associated runtime to function.
