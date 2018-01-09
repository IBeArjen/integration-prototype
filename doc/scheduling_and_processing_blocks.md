# Scheduling Blocks and Processing Blocks

From the system level C&C view §2.4.1

> Scheduling blocks are set by TM. 

> Scheduling blocks contain descriptions of Processing Blocks, which supply
> parameters for SDP processing associated with the observation. When a 
> Scheduling Block gets configured, SDP will instantiate these Processing 
> blocks.

> Any real-time Processing Blocks are then executed immediately, as they 
> directly correspond to the configured observation.

> Offline Processing Blocks will be inserted into a scheduling queue managed 
> by the SDP.

> TM can cancel offline Processing blocks as well as insert new offline
> processing blocks after the fact by configuring a Scheduling Block that
> contains no real-time Processing Blocks.


