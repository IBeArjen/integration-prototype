# Master Controller (RPyC flavour)

## Purpose

This implementation of SIP master controller emulates the SDP-TM command
interface with RPyC.

It implements the "Master Controller" component of the SDP architecture.

## Responsibilities

- Provides the SDP control interface to TM.
- Implements the TM mandated states.
- Monitors the SDP service tasks and changes state as appropriate.
- Forwards processing block device creation command to the processing block
 controller.

## Provided interfaces

The following functions are exposed with RPyC on port *\[TBD]*:

- online()
- offline()
- shutdown()
- attribute_value = get_attribute(attribute_name)
- processing_block_id = create_processing_device(processing_type,
  subarray, observing_block)

## Required interfaces

- processing block controller

*NOTE(BM): Need to consider this carefully as hopefully we don't **need** the 
processing controller to run this service. If so required interfaces will be 
none*

## Dependencies

Python packages:

- rpyc
- dockerpy *Note(BM): will this still be needed after the refactor?*
