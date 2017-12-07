# Master Controller Service

## Purpose

Implementations of the "Master Controller" component of the SDP
architecture.

This is the SDP Element Master as defined in the SKA control system
guidelines document.

## Responsibilities

- Entry-point to TM to retrieve high level information on the system
- Primary point of control (interface to TM) for general SDP
  operations
- Provides rolled-up monitoring and reporting as well as overall SDP
  status. This is provided though a number of state attributes.
    - ***state***:
    - ***adminMode***:
    - ***healthState***:
    - ***obsState***:
- Exposes a command interface to TM which includes, but is not limited
  to, the following commands defined in ICDs (§5.1.4.4), SKA control
  system guidelines, and SKA Tango Developers guide, (§6.10):
    - ***state***
    - ***init***
    - ***standby***
    - ***disable***
    - ***offline***: *SIP only command*
    - ***shutdown***: *SIP only command*
    - ***on*** or ***online***
    - ***get_capacity***: *Defined in the SDP-TM ICDs*
    - ***new_processing_block***: *Defined in the SDP-TM ICDs*
    - ***delete_processing_block***: *Defined in the SDP-TM ICDs*

## References

1. [SDP System-Level Module Decomposition View (§2.1.1.1)](https://docs.google.com/document/d/1M0S20FWn4Dsb8nl9duIoW93OEiXlzVDGh8sqImOl6S0)
1. [SDP System-Level C&C View (§2.1)](https://docs.google.com/document/d/1FTGfuy1R4_xjEug5ENPZwXqfAEy9ydqYXCXP__48KKw)
1. [SKA Control System Guidlines (000-000000-010 Rev 01)](https://ska-aw.bentley.com/SKAProd/Search/QuickLink.aspx?n=000-000000-010&t=3&d=Main%5ceB_PROD&sc=Global&r=01&i=view)
1. [SKA Tango Developers Guideline (000-000000-011 Rev 01](https://docs.google.com/document/d/1vr6xcYTpYOZnECmu47KG5cdyKMF9zE089ufBT5CprNY/edit#heading=h.gjdgxs)
1. [SDP_TM_LOW_ICD 100-000000-029_03](https://docs.google.com/document/d/13E9bgygFz5H-fPrRXSgwxQWTrGNk_yCLCE35NeLhNRs)
1. [SDP_TM_MID_ICD 300-000000-029_03](https://docs.google.com/document/d/1HI8efEahniLJZUfhZoDclump9L-SkEkD_m7kIJBgkcE)
