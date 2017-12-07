# System Services

## Description

Common interfaces in use by all SDP modules. Implementations are going to be
managed by Platform services. As changes to these modules might impact the
entire system, this should be restricted to well-established standard
interfaces.

*NOTE(BM): The description above (taken from the module view) looks like
it needs work.*
*NOTE(BM): I don't think we want any code here in SIP if at all possible!
- maybe the SIP base docker image?*

**Contains:**

- Operating System
- Storage Interface
- Logging Interface
- Accelerator Interfaces

### Operating System

Unix-like Operating System interface, offering baseline functionality such
as memory and process management.

*NOTE(BM) ... !*

### Storage Interface

Provides a common interface for access to storage. For example, Platform
Services will be expected to provide a POSIX-like file interface to Buffer data.

*NOTE(BM) ... Not sure this is useful or will stay.*

### Logging Interface

Provides the capability for processes to emit logging information for tracking
down system defects, root cause analysis, resource overconsumption etc.
This module implements a generic interface that decouples the generation of
logs from aggregation (see Logging and Health in Platform services).

*NOTE(BM) ... Not sure this is useful in this view as logging is already
captured in the Platform services sufficiently and will use standard
technologies!***

### Accelerator Interfaces

Provides access to high-performance computing capabilities. This may involve
standard parallel libraries such as OpenMP and OpenCL, but also more
specialised libraries such as CUDA.

*NOTE(BM) ... This has no place in the architecture unless we are developing
our own interfaces which would be unadvisable*

## References

- SDP System-level Module Decomposition and Dependency View, §2.1.9
