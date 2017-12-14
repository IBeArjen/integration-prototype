# Execution Control

## Description

This package groups all modules related to the control and monitoring of SDP.
It is composed of a set of sub-packages, the majority of which are 
expected to be deployable as containerised services under control of a 
container orchestration framework such as Docker Swarm.

Groups packages related to the control and monitoring of SDP.

**Contains:**

- Master Controller
- Processing Control


***Note-1: There is still a lack of detailed design in this area of the SDP 
architecture, in particular in the role and responsibilities of the 
Processing Controller and processing block devices, and in the 
communication pattern used between services. As a result we expect to 
prototype several variants of services in this component.***

***Note-2: There is also a concerning level of overlap between 
services which could sit in this package vs. those in the 
`sdp_services` and `platform_services` packages that needs 
resolving. In particular, whether monitoring and logging 
services should be sub-packages here, or the other packages noted 
in the previous sentence.***


## Reference figures

*SDP Execution Control Decomposition Diagram (version: 06/12/17)*
![](https://drive.google.com/uc?id=1l53_rVbOMbB_79ZIHrh4CfVWmngBvu2_)

*SDP-TM Tango interfaces Diagram (version: 06/12/17)*
![](https://drive.google.com/uc?id=1PeE9IYFmHGA5NpIMLGPnOkOWD8IN4dHx)

## References

1. [SDP System-level Module decomposition View](http://bit.ly/sdp_system_level_module_view)
1. [SDP System-level Component and Connector View](http://bit.ly/sdp_system_cc_view)
1. [SDP-TM Tango interfaces diagram version 06/12/17](https://drive.google.com/uc?id=1Pp96owTtlzOzmGxRaQTqfL21NMVfWUdf)
