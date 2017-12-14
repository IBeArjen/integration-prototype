# SIP Code structure

SIP code is divided into a hierarchical set of packages within the `sip` 
folder which can be categories into three main types:

- **Libraries**: Provide a collection of non-volatile modules to share resable
  code with other parts of the SDP, in particular for writing Science Pipeline
  workflows. 

- **Services**: Small, independently deployable applications which provide a 
  service or set of functions to other parts of the SIP code. 

- **Pipeline workflows**: Distributed parallel applications fulfilling the main 
  business goal of the SDP, ie processing science data from the telescope.
  These will be written using core processing library components and an 
  execution framework chosen to meet the requirements of the particular 
  workflow. 
  These should be independently deployable for testing, but in production will
  interface with a set of other SDP services which consume and / or provide
  data to the rest of the system or subsequent stages of data processing.

 
Each package should be self contained, documented and independently testable.
