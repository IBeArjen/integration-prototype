# Master Controller Service

## Purpose

Implementations of the "Master Controller" component of the SDP
architecture.

This is the SDP Element Master as defined in the SKA control system
guidelines document.

## Responsibilities

- Entrypoint to Tm to retrieve high level information on the system
- Primary point of control (interface to TM) for general SDP
  operations
- Provides rolled-up monitoring and reporting as well as overall SDP
  status (to TM)
- Exposes a command interface to TM with the following commands:
    - online
    - offline
    - shutdown
    - get_attribute
    - create_processing_device

## References

- [SDP System-Level Module Decomposition View (§2.1.1.1)](https://docs.google.com/document/d/1M0S20FWn4Dsb8nl9duIoW93OEiXlzVDGh8sqImOl6S0)
- [SDP System-Level C&C View (§2.1)](https://docs.google.com/document/d/1FTGfuy1R4_xjEug5ENPZwXqfAEy9ydqYXCXP__48KKw)
- [SKA Control System Guidlines, 000-000000-010 Rev 01](https://ska-aw.bentley.com/SKAProd/Search/QuickLink.aspx?n=000-000000-010&t=3&d=Main%5ceB_PROD&sc=Global&r=01&i=view)
