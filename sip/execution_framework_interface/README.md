# Execution Framework Interface

## Description

This package contains a library which provides a common interface to 
execution frameworks. This library is used by the Processing Controller Service
to run Science Pipeline workflows without having to know about the details of 
the particular Execution Framework implementation being run against. 

***Note: In a microservices architecture, this library could, and probably 
should, be developed as part of the Processing controller service as it will 
not be used elsewhere. We are including it in SIP as a separate package to be 
consistent with the SDP architecture.** 


