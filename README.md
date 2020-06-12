# CSV to Nested Json Converter

Keboola Connection processor for converting a CSV file to a JSON file. Currently supports three levels of nesting.



## Usage
This processor currently allows for converting a CSV file located in `data/in/tables` to a JSON file 
that will be stored in `data/out/files`. 
This processor supports nesting (three levels) and three datatypes:

- `bool` -  Boolean value (accepts `'True'` and `'False'`)
- `string` - String
- `number` - Number
- `object` - Object - valid JSON array or JSON object, e.g. ["1","2"], {"key":"val"}

When using this processor, you need to specify all columns and datatypes you want them to have in the JSON file - 
if you want the value to be enclosed in double quotes, use `string`, 
if you want the value to be numeric, use `number`. 
If you want it to be Boolean, use `bool` 
(this processor accepts `'True'` and `'False'` as boolean values on the input - the default Keboola Connection Boolean values 
when the column type is specified to be Boolean.)

## Config

You need to specify two parameters - delimiter, and column types.

The value of delimiter will be the character you want to nest on - ie. if you had columns _adress\_street_ and _adress\_city_ and you set the delimiter to `_`, 
the result would be a `[{address:{street:street_value, city:city_value}}]`. 
As of now, the processor supports up to three levels of nesting (so you can't have more than three delimiter values in the column name),
 and single character delimiters.

In the column types you need to specify the datatypes for all the columns in your CSV file. 
You can choose from string (value enclosed in double quotes), number (value not enclosed in double quotes), and boolean (True X False).

## Sample Config

A sample config looks like this:

```
{
  "storage": {
    "input": {
      "files": [],
      "tables": []
    },
    "output": {
      "files": [],
      "tables": []
    }
  },
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
           "type":"string"},
          {"column":"id2",
           "type":"string"},
          {"column":"time_11",
           "type":"bool"},
            {"column":"time_reviewed_r2",
              "type":"bool"},
          {"column":"time_reviewed_r1_r1",
                "type":"bool"}
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
    "bool": {
      "bool1": true,
      "bool2": 1
    },
    "time": {
      "11": true,
      "submitted": "2019-08-13T19:05:45Z",
      "reviewed": {
        "r2": true,
        "r1": {
          "r1": true,
          "r2": true
        }
      }
    },
    "id2": "mh53bpv123456t2ljkk04jlg",
    "ansconcat": "Jan Palek",
    "field.id": "123456",
    "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx"
  },
  {
    "bool": {
      "bool1": true,
      "bool2": 1
    },
    "time": {
      "11": true,
      "submitted": "2019-08-13T19:05:45Z",
      "reviewed": {
        "r2": true,
        "r1": {
          "r1": true,
          "r2": true
        }
      }
    },
    "id2": "mh53bpv123456t2ljkk04jlg",
    "ansconcat": "Jan Palek",
    "field.id": "123456",
    "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx"
  },
  {
    "bool": {
      "bool1": true,
      "bool2": 1
    },
    "time": {
      "11": true,
      "submitted": "2019-08-13T19:05:45Z",
      "reviewed": {
        "r2": true,
        "r1": {
          "r1": true,
          "r2": true
        }
      }
    },
    "id2": "mh53bpv123456t2ljkk04jlg",
    "ansconcat": "Jan Palek",
    "field.id": "123456",
    "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx"
  },
  {
    "bool": {
      "bool1": true,
      "bool2": 1
    },
    "time": {
      "11": true,
      "submitted": "2019-08-13T19:05:45Z",
      "reviewed": {
        "r2": true,
        "r1": {
          "r1": true,
          "r2": true
        }
      }
    },
    "id2": "mh53bpv123456t2ljkk04jlg",
    "ansconcat": "Jan Palek",
    "field.id": "123456",
    "id": "https://keboolavancouver.typeform.com/to/XXXX?id=xxxxx"
  }
]
```