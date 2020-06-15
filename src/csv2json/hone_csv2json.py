# from hone.utils import csv_utils
import ast
import copy
import logging
import sys

import hone
import strconv


class Csv2JsonConverter(hone.Hone):
    """
    Customized csv to json converter. Tied with the csv file allowing converting row by row.
    """

    def __init__(self, delimit, csv_file_path):
        hone.Hone.__init__(self)
        self.delimit_chars = delimit
        self.set_csv_filepath(csv_file_path)
        self.column_names = self.csv.get_column_names()
        self.column_struct = self.generate_full_structure(self.column_names)
        self.str_converter = strconv.Strconv()
        self._setup_converter()

    def convert_object(self, s):
        s = s.strip()
        if s == "":
            return None
        try:
            if (s.startswith('{') and s.endswith('}')) or (s.startswith('[') and s.endswith(']')):
                return ast.literal_eval(s)
            else:
                raise ValueError(f'{s}Not object type.')
        except Exception:
            raise ValueError(f'{s}Not object type.')

    def _setup_converter(self):
        self.str_converter.register_converter('obj', self.convert_object)
        self.str_converter.register_converter('int', strconv.convert_int)
        self.str_converter.register_converter('float', strconv.convert_float)
        self.str_converter.register_converter('bool', strconv.convert_bool)

    def convert_row(self, row, coltypes, delimit, infer_undefined=False):
        data = row
        json_struct = self.populate_structure_with_data(data, coltypes, delimit, infer_undefined)
        return json_struct

    def populate_structure_with_data(self, row, coltypes, delimit, infer_undefined=False):
        # TODO: add recursion to enable "unlimited" levels
        json_struct = []
        num_columns = len(self.column_names)
        processed_row = row
        json_row = copy.deepcopy(self.column_struct)
        i = 0
        while i < num_columns:
            cell = processed_row[i].replace('\'', '\\\'')
            column_name = self.column_names[i]
            c_name_splitted = column_name.split(delimit)
            cell = self._convert_datatype(cell, coltypes, column_name, True)

            self._fill_value_on_level(json_row, c_name_splitted, cell)
            i += 1
        json_struct.append(json_row)
        return json_struct

    def _convert_datatype(self, cell, coltypes, column_name, infer_undefined=False):
        cell = cell.strip()
        colnames = [ct['column'] for ct in coltypes]
        # if set to infer infer all undefined fields
        if infer_undefined and column_name not in colnames:
            cell = self.str_converter.convert(cell)
        try:
            for j in coltypes:
                if (str(j["column"])) == column_name:
                    if j["type"] == 'number':
                        cell = strconv.convert_float(cell.strip())
                    elif j["type"] == 'string':
                        pass
                    elif j["type"] == 'bool':
                        cell = strconv.convert_bool(cell)
                    elif j["type"] == 'object':
                        if cell:
                            cell = self.convert_object(cell)
                    else:
                        logging.info(
                            'datatype for %s is not set, treating it as a string' % column_name)
        except ValueError:
            logging.exception(f'The value {cell} does not match the type: {j["type"]}')
            sys.exit(1)
        return cell

    def _fill_value_on_level(self, json_row, c_name_splitted, cell):
        if len(c_name_splitted) == 1:
            json_row[c_name_splitted[0]] = cell
        elif len(c_name_splitted) == 2:
            json_row[c_name_splitted[0]][c_name_splitted[1]] = cell
        elif len(c_name_splitted) == 3:
            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]] = cell
        elif len(c_name_splitted) == 4:
            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]][
                c_name_splitted[3]] = cell
        else:
            logging.info("Too many nesting levels!")
            sys.exit(1)

    def get_schema(self, csv_filepath):
        self.set_csv_filepath(csv_filepath)
        column_names = self.csv.get_column_names()
        column_struct = self.generate_full_structure(column_names)
        return column_struct, column_names
