# Science Pipeline Workflows

## Description

This package will contain a set of Science Pipeline Workflows applications.

Science Pipeline Workflows are data driven workflows, expressed in a terms of 
an Execution Framework API and make use of Core Processing functions or 
Processing Wrappers provided by the Execution Framework implementation.  

Science Pipeline workflows will be executed by the Workflow Engine 
(*in the Processing Controller?*) using an Execution Framework runtime.

The expected steps necessary to execute a data-driven workflow, will
typically involve:

- Configuring the buffer to provide required Data Islands
- Creating Data queues for dynamic data
- Initialising Quality Assessment to generate appropriate metrics
- Using Model Database to extract a Science Data Model
- Employing Execution Framework instances to execute workflows on available
  processing resources.
- Update the Science Data Product Catalogue in the Data Preparation and
  Delivery

***Note: In the SIP code we expect to have a small number of example 
demonstration pipeline workflows in this package whose main role is to 
provide a platform for exercising interfaces with services in the SIP SDP 
software stack.***
