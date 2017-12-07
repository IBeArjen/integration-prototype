# Execution Frameworks

## Description

Components responsible for the execution of compatible Science Pipeline
Workflows.

The SDP will support multiple (independently developed and maintained)
execution frameworks.

***NOTE(BM): In SIP code the expectation is that this package will contain
very little, if any actual code.***

**Contains:**

- Execution Framework Interface
- Execution Framework Implementations (if not COTS)
- Processing Wrappers

### Execution Framework Interface

Provides a common interface to manage the interaction between the Processing
Controller and Execution Framework implementations.

*NOTE(BM): This sounds like it should sit in the execution_control?!*

### Execution Framework Implementations

Implementations of execution frameworks or code modifying / wrapping other
COTS execution frameworks for the purposes of running SDP Science Workflow
Pipelines.

Could also be forks or scripts used to deploy or provision and Execution
Framework.

### Processing Wrappers

Wraps Processing Components, Receive and SDP service interfaces for SDP
Science Pipeline Workflows and the Execution Framework Implementation.

*NOTE(BM): The description in the module decomposition view is concerning.*
