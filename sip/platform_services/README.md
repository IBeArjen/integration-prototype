# Platform services

## Description

This package groups sub-packages which provide non-domain specific
services. It is expected that this will be implemented mostly using configured 
off-the-shelf components.

***Note: The separation between packages in `platform_services`, 
`execution_control`, and `sdp_services` is still fairly poorly defined in the 
SDP architecture so some packages here may move in the future. 

**Contains:**

- Compute Provisioning
- Storage Provisioning
- Service Provisioning
- Configuration and Coordination
- Logging and Health
- Data Queues

### Compute Provisioning

Provides the compute infrastructure to SDP modules to run applications in
certain environments. This will encompass mechanisms for software defined
infrastructure management (IaaS), hardware configuration and management,
deployment automation as well as inventory management.

### Storage Provisioning

Provides the storage infrastructure to SDP modules. Storage may use
block, file or object technology.

Most provisioning will involve Buffer Services (from SDP Services?)

### Service Provisioning

Provides a set of standard services to the SDP that ...?

*NOTE(BM): Not sure the SDP system-level module view has a useful description.*

### Data Queues

Real-time service for streaming data between workflows and services. Used
for loose coordination between executing workflows as well as publishing
calibration solutions, alerts and QA data.

*NOTE(BM): Could also be used for an event queue?*

### Configuration & Coordination

High available database storing SDP configuration information. Used
for coordinating platform-wide behaviour, such as registry/discovery,
orchestration as well as to provide a consistent picture of the SDP state.
Should support scalable guaranteed notifications on configuration changes.

### Logging and Health

Collects and aggregates health information from all SDP infrastructure, such as
compute, storage and networking. Provides fine-grained views into the system
health both for local operations as well as Execution Control modules.

This is different to monitoring (in Execution Control) as it is not expected to
implement action based on this information.

*NOTE(BM): Need to clarify the definition of monitoring which sits in
execution control.*
