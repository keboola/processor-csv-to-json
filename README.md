# CSV to Nested Json Converter

Keboola Connection processor for converting a CSV file to a JSON file.



## Usage
This processor currently allows for converting CSV files located in `data/in/tables` to JSON files 
that will be stored in `data/out/files`. 

This processor supports datatypes:

- `bool` -  Boolean value  case-insensitive conversion: `t`, `true`, `yes` to `True` and `f`, `false`, `no` to `False`
- `string` - String
- `number` - Number
- `object` - Object - valid JSON array or JSON object, e.g. ["1","2"], {"key":"val"}, (1, 2)

When using this processor, you can specify te datatype for only a subset (or none) of the columns.

Columns that do not have explicitly defined datatypes will be converted to:

- String if `infer_undefined` is set to `false` or omitted
- Datatype will be inferred from the value itself if `infer_undefined` is set to `true`

## Config

You need to specify the delimiter. The delimiter can be a multicharacter string (e.g. '||'). You can also specify the column types, currently there are four supported data types - number, string, bool, and object. If you don't specify these, the processor will attempt to identify the datatype by itself. You can also specify the datatype only for a subset of the columns.

The value of delimiter will be the character you want to nest on - ie. if you had columns _adress\_street_ and _adress\_city_ and you set the delimiter to `_`, the result would be a `[{address:{street:street_value, city:city_value}}]`. If there are two delimiters next to each other (e.g. _adress\_\_street_), the extractor will return a user error.

## Sample Config

A sample config looks like this:

```
{
  "parameters": {
      "delimiter" : "_"
      ,"column_types":[
          {"column":"bool_bool2",
           "type":"number"},
           {"column":"bool_bool1",
            "type":"bool"},
          {"column":"id",
           "type":"string"},
          {"column":"field.id",
           "type":"string"},
          {"column":"ansconcat",
           "type":"string"},
          {"column":"time_submitted",
           "type":"string"}
      ]
  },
  "image_parameters": {}
}
```
with this table:

time_reviewed_r1_r2|time_reviewed_r1_r1|time_reviewed_r2|id|field.id|ansconcat|time_submitted|id2| time_11| bool_bool2|bool_bool1
-----|-----|-----|-----|-----|-----|-----|-----| -----| -----|-----
True|True|True|https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx|123456|Jan Palek|2019-08-13T19:05:45Z|mh53bpv123456t2ljkk04jlg|True|1|True
True|True|True|https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx|123456|Jan Palek|2019-08-13T19:05:45Z|mh53bpv123456t2ljkk04jlg|True|1|True
True|True|True|https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx|123456|Jan Palek|2019-08-13T19:05:45Z|mh53bpv123456t2ljkk04jlg|True|1|True
True|True|True|https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx|123456|Jan Palek|2019-08-13T19:05:45Z|mh53bpv123456t2ljkk04jlg|True|1|True

will produce a JSON object like this:

```
[
    {
        "time": {
            "11": true,
            "reviewed": {
                "r1": {
                    "r2": true,
                    "r1": true
                },
                "r2": true
            },
            "submitted": "2019-08-13T19:05:45Z"
        },
        "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx",
        "field.id": "123456",
        "ansconcat": "Jan Palek",
        "id2": "mh53bpv123456t2ljkk04jlg",
        "bool": {
            "bool2": 1,
            "bool1": true
        }
    },
    {
        "time": {
            "11": true,
            "reviewed": {
                "r1": {
                    "r2": true,
                    "r1": true
                },
                "r2": true
            },
            "submitted": "2019-08-13T19:05:45Z"
        },
        "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx",
        "field.id": "123456",
        "ansconcat": "Jan Palek",
        "id2": "mh53bpv123456t2ljkk04jlg",
        "bool": {
            "bool2": 1,
            "bool1": true
        }
    },
    {
        "time": {
            "11": true,
            "reviewed": {
                "r1": {
                    "r2": true,
                    "r1": true
                },
                "r2": true
            },
            "submitted": "2019-08-13T19:05:45Z"
        },
        "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx",
        "field.id": "123456",
        "ansconcat": "Jan Palek",
        "id2": "mh53bpv123456t2ljkk04jlg",
        "bool": {
            "bool2": 1,
            "bool1": true
        }
    },
    {
        "time": {
            "11": true,
            "reviewed": {
                "r1": {
                    "r2": true,
                    "r1": true
                },
                "r2": true
            },
            "submitted": "2019-08-13T19:05:45Z"
        },
        "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx",
        "field.id": "123456",
        "ansconcat": "Jan Palek",
        "id2": "mh53bpv123456t2ljkk04jlg",
        "bool": {
            "bool2": 1,
            "bool1": true
        }
    }
]
```