import unittest

from csv2json.hone_csv2json import Csv2JsonConverter


class TestCsv2JsonConverter(unittest.TestCase):
    def test_convert_object_single_quote_passes(self):
        json_value = r"""{"somekey":"Single\'s are not a problem"}"""
        expected = {"somekey": "Single's are not a problem"}
        converter = Csv2JsonConverter([])
        results = converter.convert_object(json_value)
        self.assertDictEqual(expected, results)

    def test_convert_object_conversion_passes(self):
        json_value = '{"content":"Ttest push","defaultTranslation":true,"langs":["en"]}'
        expected = {
            "content": "Ttest push",
            "defaultTranslation": True,
            "langs": ["en"],
        }
        converter = Csv2JsonConverter([])
        results = converter.convert_object(json_value)
        self.assertDictEqual(expected, results)

    def test_convert_object_array_conversion_passes(self):
        json_value = '[{"a":"ab"}, "b"]'
        expected = [{"a": "ab"}, "b"]
        converter = Csv2JsonConverter([])
        results = converter.convert_object(json_value)
        self.assertEqual(expected, results)

    def test_convert_object_bracket_fails(self):
        json_value = "(1123)"
        converter = Csv2JsonConverter([])
        with self.assertRaises(ValueError):
            converter.convert_object(json_value)

    def test_nan_value_inferred_as_string(self):
        json_value = "NaN"
        converter = Csv2JsonConverter([])
        converted = converter.str_converter.convert(json_value)
        self.assertEqual(json_value, converted)


if __name__ == "__main__":
    unittest.main()
