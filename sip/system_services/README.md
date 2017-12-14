# System Services

## Description

This package contains sub-packages which provide libraries for common APIs
used bu all SDP modules. Extreme care should be taken in code within this 
package as it could have impact on all other modules.

***Note-1: In SIP we do not expect to have any code in this package as we will
be using entirely standard packages and modules which do not need a 
customisation.***

***NOTE-2: The description in the SDP module view architecture document looks 
like it needs work.***

**Contains:**

- Operating System
- Storage Interface
- Logging Interface
- Accelerator Interfaces

### Operating System

Unix-like Operating System interface, offering baseline functionality such
as memory and process management.

***NOTE(BM) There will be no SIP code in this (proposed) sub-package.***

### Storage Interface

Provides a common interface for access to storage. For example, Platform
Services will be expected to provide a POSIX-like file interface to Buffer data.

***NOTE(BM) There will be no SIP code in this (proposed) sub-package.***

### Logging Interface

Provides the capability for processes to emit logging information for tracking
down system defects, root cause analysis, resource overconsumption etc.
This module implements a generic interface that decouples the generation of
logs from aggregation (see Logging and Health in Platform services).

***NOTE(BM) There will be no SIP code in this (proposed) sub-package.***

### Accelerator Interfaces

Provides access to high-performance computing capabilities. This may involve
standard parallel libraries such as OpenMP and OpenCL, but also more
specialised libraries such as CUDA.

***NOTE(BM) There will be no SIP code in this (proposed) sub-package.***

## References

- SDP System-level Module Decomposition and Dependency View, §2.1.9
