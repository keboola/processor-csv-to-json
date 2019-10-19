## Usage
This processor currently allows for converting a CSV file located in `data/in/tables` to a JSON file that will be stored in `data/out/files`. This processor supports nesting (three levels) and three datatypes - Boolean, String, and Number. When using this processor, you need to specify all columns and datatypes you want them to have in the JSON file - if you want the value to be enclosed in double quotes, use `string`, if you want the value to be numeric, use `number`. If you want it to be Boolean, use `bool` (this processor accepts `'True'` and `'False'` as boolean values on the input - the default Keboola Connection Boolean values when the column type is specified to be Boolean.)

## Config

You need to specify two parameters - delimiter, and column types.

The value of delimiter will be the character you want to nest on - ie. if you had columns _adress\_street_ and _adress\_city_ and you set the delimiter to `_`, the result would be a `[{address:{street:street_value, city:city_value}}]`. As of now, the processor supports up to three levels of nesting (so you can't have more than three delimiter values in the column name), and single character delimiters.

In the column types you need to specify the datatypes for all the columns in your CSV file. You can choose from string (value enclosed in double quotes), number (value not enclosed in double quotes), and boolean (True X False).

## Sample Config

For sample config please refer to here: https://bitbucket.org/kds_consulting_team/kds-team.processor-csv-to-json/src/master/README.md