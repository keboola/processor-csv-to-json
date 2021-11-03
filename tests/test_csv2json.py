'''
Created on 12. 11. 2018

@author: esner
'''
import unittest

from csv2json.hone_csv2json import Csv2JsonConverter


class TestCsv2JsonConverter(unittest.TestCase):

    def test_convert_object_single_quote_passes(self):
        json_value = '{"somekey":"Single\'s are not a problem"}'
        expected = {"somekey": "Single's are not a problem"}
        converter = Csv2JsonConverter([])
        results = converter.convert_object(json_value)
        self.assertDictEqual(expected, results)

    def test_convert_object_bracket_fails(self):
        json_value = '(1123)'
        converter = Csv2JsonConverter([])
        with self.assertRaises(ValueError):
            converter.convert_object(json_value)


if __name__ == "__main__":
    unittest.main()
