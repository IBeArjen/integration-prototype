# SDP Services

## Description

Groups packages that provide domain specific SDP services to support processing.

As this is a data-driven architecture, this especially concerns maintaining
data items around the execution of Science Pipeline workflows.

**Contains:**

- Product Preparation and Delivery
- Quality Assessment
- Long Term Storage
- Model Database Services
- Buffer Management Services
- Data Queue Services

***NOTE(BM): At present, SIP will not be concerned with prototyping Delivery
and related services so not all of the SDP services will be considered for
the first version of the prototype.***

### Product Preparation and Delivery

Assembles final data products and delivers them to the observatory and
regional centres.
Maintains the Science Data Product Catalogue using data from Scheduling Blocks
and the Science Data Model produced by Model Databases.

### Quality Assessment

Handles the assessment of partial results from Science Pipeline Workflows to
allow previews into the quality of the final data products. This might also
involve some analysis of the data.

### Long Term Storage

The persistent background storage to the Buffer. Provides long-term storage
for data products.

### Model Database Services

Produces the Science Data Model from the Global Sky Model database and the
Tango connection to TM. Handles queries and updates to the Global Sky Model
database.

Note: This is **Model** database services rather than general a database
service / services.

### Buffer Management Services

Arranges storage of input data for workflow execution as well as Data Products.
Implements Data Island Interface for applications to access storage. Performs
light data processing tasks to prepare data access.

### Data Queue Services

Handles initialisation and management of Data Queues as required for execution
of Science Pipeline Workflows. Performs real-time forwarding of alert and
calibration data to TM.

*NOTE(BM): The description above, from the module view, is a little confusing.
There needs to be a distinction between this and any queues provided in the
platform services (if there are any defined there).*

## References

- SDP System-level Module Decomposition and Dependency View, §2.1.2
