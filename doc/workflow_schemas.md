# SIP Workflow schemas

## Visibility Ingest

### Example:

see <https://github.com/SKA-ScienceDataProcessor/sdp-par-model/blob/master/sdp_par_model/dataflow/pipeline.py>
line 204 `def create_ingest(self)`.

```json
{
    "receive": {
        "streams": [
            { "host": "127.0.0.1", "port": 2001 },
            { "host": "ingest-01", "port": 2001 },
            { "host": "ingest-01", "port": 2002 },
            { "host": "ingest-02", "port": 2001 }
        ],
    },
    "demix": { 
    
    },
    "flag": { 
    
    },
    "average": { 
    
    }
}
```

### Schema:

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Visibility ingest workflow configuration",
    "description": "Visibility Ingest Configuration",
    "type": "object",
    "required": [],
    "properties": {
        "receive": {
            "type": "object",
            "description": "Receive configuration",
            "properties": {
            
            }
        },
        "demix": {
            "type": "object",
            "description": "Demix configuration",
            "properties": {
            
            }
        },
        "flag": {
            "type": "object",
            "description": "Flagging (RFI etc) configuration",
            "properties": {
            
            }
        },
        "average": {
            "type": "object",
            "description": "Averaging configuration",
            "properties": {
            
            }
        }
    }
}
```
