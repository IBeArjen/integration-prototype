# SIP Control configuration schemas

<http://json-schema.org/>
<https://spacetelescope.github.io/understanding-json-schema/>

## Scheduling block

### Example

```json
{
    "id": 1,
    "summary": "Example Scheduling block.",
    "start": "2018-01-03T15:56:27.000000",
    "end": "2018-01-03T22:56:27.000000",
    "processing": [
        {
            "type": "vis-ingest-01", 
        },
        {
            "type": "ical"
        }    
    ]
}
```

### Schema

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Scheduling Block",
    "description": "SKA Scheduling block",
    "type": "object",
    "required": ["id", "summary", "start", "end", "processing"],
    "properties": {
        "id": {
            "description": "The unique identifier for the scheduling block",
            "type": "integer"
        },
        "summary": {
            "type": "string"
        },
        "start": {
            "format": "date-time",
            "type": "string",
            "description": "The start time for the scheduling block"
        },
        "end": {
            "format": "date-time",
            "type": "string",
            "description": "The end time for the scheduling block"
        },
        "processing": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["type"],
                "properties": {
                    "type": "string"
                }
            }
        }
    }   
}
```


## Processing block


### Examples

#### Example: Processing block for Visibility ingest

```json
{
    "id": 1,
    "type": "visibility_ingest",
    "real-time": true,
    "name": "visibility_ingest_01",
    "scheduling_block": 1,
    "configuration": {
        "input": {
            "channels": 1024,
            "baselines": 50,
            "samples": 1e8
        },
        "output": {
          "channels": 256,
          "baselines": 50,
          "samples": 1e8  
        },
        "receivers": [
            { "ip": "127.0.0.1", "port": 2001 },
            { "ip": "127.0.0.1", "port": 2002 },
            { "ip": "127.0.0.2", "port": 2001 },
            { "ip": "127.0.0.2", "port": 2002 }
        ],
        "buffer": {
            "namespace": "{{ id }}/{{ channel }}" 
        }
    }
}
```

#### Example: Processing block for ICAL

```json
{
    "id": 2,
    "type": "ICAL",
    "real-time": false,
    "name": "ICAL_01",
    "scheduling_block": 1,
    "configuration": {}
}
```

### Schema

```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Processing Block",
    "description": "SDP Processing block",
    "type": "object",
    "required": ["id", "type", "name", "summary", "configuration"],
    "properties": {
        "id": {
            "description": "The unique identifier for the processing block",
            "type": "integer"
        },
        "real-time": {
            "type": "bool",
            "description": "True if this is a real-time processing block.",  
        },
        "type": {
            "type": "string",
            "description": "Processing block type"
        },
        "name": {
            "type": "string",
            "description": "Processing block type"
        },
        "summary": {
            "type": "string"
        },
        "scheduling_block": {
            "type": "integer",
            "description": [
                "The unique identifier for the scheduling block for which ",
                "the processing block belongs"
            ]
        },
        "configuration": {
            "type": "object",
            "description": "Processing block configuration parameters"
        }
    }   
}
```

