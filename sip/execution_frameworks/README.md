# Execution Frameworks

## Description

This package contains a set of libraries and associated runtime executables,
where applicable, which provide the implementation of any custom (SDP specific)
or modified off-the-shelf execution frameworks used by the SDP.

This will also include `processing_wrappers` which wrap functions in the 
`core_processing` library, customising them to a particular execution framework
for use by Science Pipeline Workflows.

***NOTE(BM): In SIP code the expectation is that this package will contain
very little, if any actual code as we be using entirely off-the-shelf 
execution frameworks and not expecting to develop processing wrappers.
The likely exception will be any Dockerfiles or provisioning scripts specific
to a given Execution Framework.***

**Contains:**

- Execution Framework Implementations (if not purely off-the-shelf)
- Processing Wrappers

### Execution Framework Implementations

Implementations of execution frameworks or code modifying / wrapping other
COTS execution frameworks for the purposes of running SDP Science Workflow
Pipelines.

Could also be forks or scripts used to deploy or provision and Execution
Framework.

### Processing Wrappers

Wraps Processing Components, Receive and SDP service interfaces for SDP
Science Pipeline Workflows and the Execution Framework Implementation.

*NOTE(BM): The description in the module decomposition view needs review.*
