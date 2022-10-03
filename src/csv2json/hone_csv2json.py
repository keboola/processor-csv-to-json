# from hone.utils import csv_utils
import copy
import json
import logging
import sys

import hone
import strconv


class Csv2JsonConverter(hone.Hone):
    """
    Customized csv to json converter. Tied with the csv file allowing converting row by row.
    """

    def __init__(self, headers, delimiter="_"):
        self.delim_len = len(delimiter)
        hone.Hone.__init__(self, delimiters=[delimiter])
        self.column_names = headers
        self.column_struct = self.generate_full_structure(self.column_names)
        self.str_converter = strconv.Strconv()
        self._setup_converter()

    def convert_object(self, s):
        s = s.strip()
        if s == "":
            return None
        try:
            res = json.loads(s)
            if not type(res) in [list, dict]:
                raise
            return res
        except Exception:
            raise ValueError(f'{s}Not object type.')

    def _setup_converter(self):
        self.str_converter.register_converter('obj', self.convert_object)
        self.str_converter.register_converter('int', strconv.convert_int)
        self.str_converter.register_converter('float', strconv.convert_float)
        self.str_converter.register_converter('bool', strconv.convert_bool)

    def convert_row(self, row, coltypes, delimit, infer_undefined=False, colname_override=None):
        data = row
        json_struct = self.populate_structure_with_data(
            data, coltypes, delimit, infer_undefined, colname_override)
        return json_struct

    def populate_structure_with_data(self, row, coltypes, delimit, infer_undefined=False, colname_override=None):
        json_struct = []
        num_columns = len(self.column_names)
        processed_row = row
        json_row = copy.deepcopy(self.column_struct)
        if colname_override is None:
            colname_override = {}
        i = 0
        while i < num_columns:
            cell = processed_row[i].replace('\'', '\\\'')
            column_name = self.column_names[i]
            c_name_splitted = column_name.split(delimit)

            cell = self._convert_datatype(cell, coltypes, column_name, True)

            self._fill_value_on_level(json_row, c_name_splitted, cell, colname_override)
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
                        cell = self.convert_bool(cell)
                    elif j["type"] == 'object':
                        if cell:
                            cell = self.convert_object(cell)
                    else:
                        logging.info(
                            'datatype for %s is not set, treating it as a string' % column_name)
        except ValueError:
            logging.exception(
                f'The value {cell} does not match the type: {j["type"]}')
            sys.exit(1)
        return cell

    def _fill_value_on_level(self, json_row, c_name_splitted, cell, colname_override):
        if len(c_name_splitted) == 1:
            # in case of rename drop original
            orig_colname = json_row[c_name_splitted[0]]
            colname = c_name_splitted[0]
            if colname_override.get(orig_colname):
                json_row.pop(colname, None)
                colname = colname_override.get(orig_colname)

            json_row[colname] = cell
        else:
            self._fill_value_on_level(
                json_row[c_name_splitted[0]], c_name_splitted[1:], cell, colname_override)

    def get_schema(self, csv_filepath):
        self.set_csv_filepath(csv_filepath)
        column_names = self.csv.get_column_names()
        column_struct = self.generate_full_structure(column_names)
        return column_struct, column_names

    '''
    Generate recursively-nested JSON structure from column_names.
    '''

    def generate_full_structure(self, column_names):
        visited = set()
        structure = {}
        # sorted(column_names)
        # column_names = column_names[::-1]
        for c1 in column_names:
            if (str(self.delimiters[0] + self.delimiters[0]) in c1):
                logging.error(
                    f"In the column name \"{c1}\" there are two delimiters next to each other, \
which would result in an empty key. Aborting the conversion.")
                sys.exit(1)
            if c1 in visited:
                continue
            splits = self.get_valid_splits(c1)
            for split in splits:
                nodes = {split: {}}
                if split in column_names:
                    continue
                for c2 in column_names:
                    if c2 not in visited and self.is_valid_prefix(split, c2):
                        nodes[split][self.get_split_suffix(split, c2)] = c2
                if len(nodes[split].keys()) >= 1:
                    structure[split] = self.get_nested_structure(nodes[split])
                    for val in nodes[split].values():
                        visited.add(val)
            if c1 not in visited:  # if column_name not nestable
                structure[c1] = c1
        return structure

    '''
    Generate nested JSON structure given parent structure generated from initial call to get_full_structure
    '''

    def get_nested_structure(self, parent_structure):
        column_names = list(parent_structure.keys())
        visited = set()
        structure = {}
        sorted(column_names, reverse=True)
        for c1 in column_names:
            if c1 in visited:
                continue
            splits = self.get_valid_splits(c1)
            for split in splits:
                nodes = {split: {}}
                if split in column_names:
                    continue
                for c2 in column_names:
                    if c2 not in visited and self.is_valid_prefix(split, c2):
                        nodes[split][self.get_split_suffix(
                            split, c2)] = parent_structure[c2]
                        visited.add(c2)
                if len(nodes[split].keys()) >= 1:
                    structure[split] = self.get_nested_structure(nodes[split])
            if c1 not in visited:  # if column_name not nestable
                structure[c1] = parent_structure[c1]
        return structure

    '''
    Returns all valid splits for a given column name in descending order by length
    '''

    def get_valid_splits(self, column_name):
        splits = []
        i = len(column_name) - self.delim_len
        while i >= 0:
            c = column_name[i:i + self.delim_len]
            if c in self.delimiters:
                split = self.clean_split(column_name[0:i])
                splits.append(split)
            i -= 1
        return sorted(list(set(splits)))

    '''
    Returns true if str_a is a valid prefix of str_b
    '''

    def is_valid_prefix(self, prefix, base):
        if base.startswith(prefix):
            if base[len(prefix):len(prefix) + self.delim_len] in self.delimiters:
                return True
        return False

    '''
    Returns string after split without delimiting characters.
    '''

    def get_split_suffix(self, split, column_name=""):
        suffix = column_name[len(split) + self.delim_len:]
        i = 0
        while i < len(suffix):
            c = suffix[i]
            if c not in self.delimiters:
                return suffix[i:]
            i += 1
        return suffix

    def convert_bool(self, cell):
        converted = None
        try:
            converted = strconv.convert_bool(cell)
        except ValueError:
            pass

        try:
            if int(cell) == 1:
                converted = True
            elif int(cell) == 0:
                converted = False
        except ValueError:
            pass

        if converted is None:
            raise ValueError(f"Unable to convert value {cell} to boolean!")

        return converted
