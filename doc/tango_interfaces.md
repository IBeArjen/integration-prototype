# SIP Tango Interfaces

SDP will be controlled and monitored using an Tango interface, as such we
will need to prototype the following devices (also shown in the figure below):

1. Element Master
1. Element Alarms Handler
1. Element Logger
1. Element TelModel
1. Element Sub-array Node (1..16)
1. Element DataBase
1. Quality Assessment
1. Offline Processing Block (1..N)
1. Real-time Processing Block (1..N)
1. Processing Controller (C&C view [1], fig2)
1. Monitoring (C&C view [1], fig2)
1. Real-time Calibration Queue
1. Science Events Queue 

We may also want to consider the following devices:

- Tango Starter \[if using the Tango sub-system to manage Tango device servers]
- Historical DataBase, HDB++ \[if a SDP local Tango archive is required]


Devices are created by a Tango device server [3] `run()` or `server_run()` method 
or by calling the `run_server()` method of the Tango `Device` class [4].

Some of these devices types will have need multiple active concurrent device 
instances. At the moment this is limited to:

- Sub-array Node device: up to 16 devices, 1 per active sub-array.
- Offline Processing block devices: between 1 and N devices, 1 per active 
  offline processing task. These could be allocated from a pool.<br>
  *TBC: N is expected to be fairly large O(1000)?*
- Real-time Processing block devices: between 1 and N devices, 1 per active 
  real-time processing task. These could be allocated from a pool.
  *TBC: N is expected to be fairly large O(100)?*


*SIP Tango devices:*
![](https://drive.google.com/uc?id=1uxdQVvqX6JMqtTeD8rcrmXXYutXoRpVW)

*Tango Device Server Model class diagram (from <http://tango-controls.readthedocs.io/en/latest/overview/SimplifiedTangoDatamodel.html>):*
![](http://tango-controls.readthedocs.io/en/latest/_images/image2.jpg)

References

1. [SDP C&C View](http://bit.ly/sdp_system_cc_view)
1. [SDP-TM Tango interfaces diagram version 06/12/17](https://drive.google.com/uc?id=1Pp96owTtlzOzmGxRaQTqfL21NMVfWUdf)
1. [PyTango high level server API](http://pytango.readthedocs.io/en/stable/server_api/server.html)
1. [PyTango Device API](http://pytango.readthedocs.io/en/stable/server_api/server.html#tango.server.Device)
1. [SKA Control System Guidlines (000-000000-010 Rev 01)](https://ska-aw.bentley.com/SKAProd/Search/QuickLink.aspx?n=000-000000-010&t=3&d=Main%5ceB_PROD&sc=Global&r=01&i=view)
1. [SKA Tango Developers Guideline (000-000000-011 Rev 01](https://docs.google.com/document/d/1vr6xcYTpYOZnECmu47KG5cdyKMF9zE089ufBT5CprNY/edit#heading=h.gjdgxs)


