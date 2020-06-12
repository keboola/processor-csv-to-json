# from hone.utils import csv_utils
import copy
import logging
import sys

import hone


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

    def convert_row(self, row, coltypes, delimit):
        data = row
        json_struct = self.populate_structure_with_data(data, coltypes, delimit)
        return json_struct

    def populate_structure_with_data(self, row, coltypes, delimit):
        # TODO: add recursion to enable "unlimited" levels
        # TODO: add datatype inference
        json_struct = []
        num_columns = len(self.column_names)
        processed_row = row
        json_row = copy.deepcopy(self.column_struct)
        i = 0
        while i < num_columns:
            cell = processed_row[i].replace('\'', '\\\'')
            column_name = self.column_names[i]
            c_name_splitted = column_name.split(delimit)
            for j in coltypes:
                if (str(j["column"])) == column_name:
                    if j["type"] == 'number':
                        cell = float(cell.strip())
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

                    elif j["type"] == 'string':

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

                    elif j["type"] == 'bool':

                        if cell == 'True':
                            cell = True
                        elif cell == 'False':
                            cell = False
                        else:
                            logging.info(
                                "Value provided for boolean is not True or False. Please set the column\
                                     in storage to type boolean!")
                            sys.exit(1)
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
                    else:
                        logging.info(
                            'datatype for %s is not set, treating it as a string' % column_name)
            i += 1
        json_struct.append(json_row)
        return json_struct

    def get_schema(self, csv_filepath):
        self.set_csv_filepath(csv_filepath)
        column_names = self.csv.get_column_names()
        column_struct = self.generate_full_structure(column_names)
        return column_struct, column_names
