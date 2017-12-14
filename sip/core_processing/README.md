# SIP Core Processing Packages

## Description

This package contains a library of core, domain-specific, low level functions 
needed to construct the data processing and data receive pipelines and 
workflows.

Sub-packages in this folder are used (where appropriate) to divide modules into
groups of functions with a common role. Sub-packages in this folder
will evolve over time as new functions are identified and added.

**Contains:**

- Processing components library
- Receive components library

***NOTE: In SIP, most of the functions of the processing library will be 
provided by ARL and therefore we do not expect very much code in this 
package*** 


### Processing Library

A library of radio astronomy and interferometry algorithm implementations
consuming and producing data according to SDP (in memory) Data Models.

These should implement a standardised processing component interface to
make them as much as possible agnostic to how they are used in Science
Pipeline Workflows or what Execution Framework is calling them.

### Receive library

A library of functions for receiving data from CSP and LFAA (for transient
buffer data). Received data will be both written to the buffer for offline
processing as well as handed directly to real-time processing pipelines.

*NOTE(BM):  Not sure this description is correct as we probably don't want
these functions writing to the buffer.*
