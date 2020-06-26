## Usage
This processor allows for converting CSV files located in `data/in/tables` to JSON files that will be stored in `data/out/files`.

## Config

You need to specify the delimiter. The delimiter can be a multicharacter string (e.g. '||'). You can also specify the column types, currently there are four supported data types - number, string, bool, and object. If you don't specify these, the processor will attempt to identify the datatype by itself. You can also specify the datatype only for a subset of the columns.

The value of delimiter will be the character you want to nest on - ie. if you had columns _adress\_street_ and _adress\_city_ and you set the delimiter to `_`, the result would be a `[{address:{street:street_value, city:city_value}}]`. If there are two delimiters next to each other (e.g. _adress\_\_street_), the extractor will return a user error.

## Sample Config

For sample config please refer to here: https://bitbucket.org/kds_consulting_team/kds-team.processor-csv-to-json/src/master/README.md