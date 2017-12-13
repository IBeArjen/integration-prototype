# SIP top level packages

SIP has the following top level packages which are derived from the SDP 
System-level Module Decomposition and Dependency View \[1]. These are described
below:

### `core_processing`

This package contains a **library** of core domain-specific low level functions 
needed to construct the data processing and data receive pipelines and 
workflows.

Sub-packages in this folder are used (where appropriate) to divide modules into
groups of functions with a common role. Sub-packages in this folder
will evolve over time as new functions are identified and added.

##### NOTE

In the SIP code found in this repository, do not expect there will be many 
modules in this package as we are using the ARL library \[2] to provide almost
all of the functionality of this package.


### `data_models`

This package contains a library of modules which provide both in-memory and 
buffer (file format) representations SDP data models. It will also contain
functions and classes that support conversion between data formats of different
types or different versions.

##### NOTE

In SIP code as we are using ARL to provide most, if not all of the 
`core_processing` functionality it is very likely that we will have to adopt
data models from ARL and therefore potentially deviate from those in the SDP
architecture. This should be reviewed over time.


### `execution_control`

This package groups all modules related to the control and monitoring of SDP.
As such it is composed of a set of sub-packages, the majority of which are 
expected to be deployable as containerised services under control of a 
container orchestration framework such as Docker Swarm.

##### NOTE

We are still lacking detailed design of several sub-packages in this area, in
particular around the Processing Controller and how messages, such as commands, 
are sent between services.


### `execution_framework_interface`

This package contains a library which provides a common interface to 
execution frameworks. This library is used by the Processing Controller Service
to run Science Pipeline workflows without having to know about the details of 
the particular Execution Framework implementation being run against. 

##### NOTE

In a microservices architecture this library could, and probably should,
be developed as part of the Processing controller service as it will not be
used elsewhere. We are including it in SIP as a separate package to be 
consistent with the SDP architecture. 


### `execution_frameworks`

This package contains a set of libraries and associated runtime executables,
where applicable, which provide the implementation of any custom (SDP specific)
or modified off-the-shelf execution frameworks used by the SDP.

This will also include `processing_wrappers` which wrap functions in the 
`core_processing` library, customising them to a particular execution framework
for use by Science Pipeline Workflows.


##### NOTE

The SIP definition of an Execution Framework is:

> Library API (as associated runtime) responsible for execution of distributed
> Science Pipeline Workflows on a set of allocated, provisioned compute 
> resources.
>
> An execution framework provides an API for building high performance parallel
> workflow applications, by providing support for communication of data between
> processing resources connected to a fast, low-latency network, and support 
> for in-memory computing operations. The memory model provided by this API 
> should not preclude the use of accelerators (eg. GPUs).

In SIP we do not expect to have much, if any, code in this package as we are 
initially focusing on entirely off-the-shelf execution frameworks and do not
have any need for processing wrappers for the small number of example 
Science Pipeline Workflows we are developing.

### `pipeline_workflows`

This package will contain a set of Science Pipeline Workflows applications.

Science Pipeline Workflows are data driven workflows expressed in a terms of 
a Execution Framework API and making use of Core Processing functions or 
Processing Wrappers provided by the Execution Framework implementation.  

##### NOTE

In the SIP code we expect to have a small number of example demonstration 
pipeline workflows in this package whose main role is to provide a platform 
for exercising interfaces with services in the SIP SDP software stack. 

### `platform_services`



### `sdp_services`
### `system_services`


## References

1. [SDP System-level Module Decomposition and Dependency View](http://bit.ly/sdp_system_level_module_view)
1. [SDP Algorithm Reference Library](https://github.com/SKA-ScienceDataProcessor/algorithm-reference-library)
1. [SIP Glossary and Terminology](https://confluence.ska-sdp.org/display/WBS/SIP+Glossary+and+Terminology) 
