'''
Template Component main class.

'''

import logging
import sys
import hone
from hone.utils import csv_utils
import copy
import json
import csv
import os
import glob
import ntpath

from kbc.env_handler import KBCEnvHandler


# #### Keep for debug
KEY_DELIMITER = 'delimiter'
KEY_COLUMN_TYPES = 'column_types'
MANDATORY_PARS = [KEY_DELIMITER]

APP_VERSION = '0.0.1'


class MyHone(hone.Hone):
    
    def __init__(self, delimit):
        hone.Hone.__init__(self)
        self.delimit_chars = delimit
        self.csv_filepath = None
    
    def convert(self, csv_filepath, schema, colnames, row, coltypes, delimit):
        self.set_csv_filepath(csv_filepath)
        column_names = colnames
        data = row
        column_schema = schema
        json_struct = self.populate_structure_with_data(column_schema, column_names, data, coltypes, delimit)
        return json_struct
        
    def populate_structure_with_data(self, structure, column_names, row, coltypes, delimit):
        json_struct = []
        num_columns = len(column_names)
        processed_row = row
        json_row = copy.deepcopy(structure)
        print(json_row)
        i = 0
        while i < num_columns:
            cell = processed_row[i].replace('\'', '\\\'')
            column_name = column_names[i]
            c_name_splitted = column_name.split(delimit)
            for j in coltypes:
                if (str(j["column"])) == column_name:                        
                    if j["type"] == 'number':
                        cell = float(cell.strip())
                        if(len(c_name_splitted) == 1):
                            json_row[c_name_splitted[0]] = cell
                        elif(len(c_name_splitted) == 2):
                            json_row[c_name_splitted[0]][c_name_splitted[1]] = cell
                        elif(len(c_name_splitted) == 3):     
                            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]] = cell
                        elif(len(c_name_splitted) == 4):     
                            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]][c_name_splitted[3]] = cell
                        else:
                            logging.info("Too many nesting levels!")
                            sys.exit(1)
                            
                    elif j["type"] == 'string':

                        if(len(c_name_splitted) == 1):
                            json_row[c_name_splitted[0]] = cell
                        elif(len(c_name_splitted) == 2):
                            json_row[c_name_splitted[0]][c_name_splitted[1]] = cell
                        elif(len(c_name_splitted) == 3):     
                            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]] = cell
                        elif(len(c_name_splitted) == 4):     
                            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]][c_name_splitted[3]] = cell
                        else:
                            logging.info("Too many nesting levels!")
                            sys.exit(1)
                            
                    elif j["type"] == 'bool':
                        
                        if cell == 'True':
                            cell = True
                        elif cell == 'False':
                            cell = False
                        else:
                            logging.info("Value provided for boolean is not True or False. Please set the column in storage to type boolean!")
                            sys.exit(1)
                        if(len(c_name_splitted) == 1):
                            json_row[c_name_splitted[0]] = cell
                        elif(len(c_name_splitted) == 2):
                            json_row[c_name_splitted[0]][c_name_splitted[1]] = cell
                        elif(len(c_name_splitted) == 3):     
                            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]] = cell
                        elif(len(c_name_splitted) == 4):     
                            json_row[c_name_splitted[0]][c_name_splitted[1]][c_name_splitted[2]][c_name_splitted[3]] = cell
                        else:
                            logging.info("Too many nesting levels!")
                            sys.exit(1)
                    else:
                        logging.info('datatype for %s is not set, treating it as a string' % column_name)        
            i += 1
        json_struct.append(json_row)
        return json_struct
    
    def get_schema(self, csv_filepath):
        self.set_csv_filepath(csv_filepath)
        column_names = self.csv.get_column_names()
        column_struct = self.generate_full_structure(column_names)
        return column_struct, column_names

class Component(KBCEnvHandler):
    def __init__(self):
        KBCEnvHandler.__init__(self, MANDATORY_PARS, data_path='data/')
        self.validate_config(MANDATORY_PARS)
        self.delimiter = self.cfg_params[KEY_DELIMITER]
        self.column_types = self.cfg_params.get(KEY_COLUMN_TYPES)

        self.Hone = MyHone(delimit = self.delimiter)
        self.input_tables  = glob.glob(self.tables_in_path + "/*[!.manifest]")
        
        self.set_default_logger(logging.INFO)
       
        logging.info('Loading configuration...')

    def run(self):
        for file in self.input_tables:
            logging.info("Processing table %s" % file)
            mh = MyHone(delimit = self.delimiter)
            schema, columns = mh.get_schema(file) 
            # returns nested JSON schema for input.csv
            with open(file, mode='rt', encoding='utf-8') as in_file, open(self.tables_out_path + '/' + ntpath.basename(file).replace('.csv', '')  + '.json', mode='wt', encoding='utf-8') as out_file:
                lazy_lines = (line.replace('\0', '') for line in in_file)
                reader = csv.reader(lazy_lines, lineterminator='\n')
                out_file.write('[')
                logging.info("[ written")
                next(reader, None)
                for row in reader:
                    result = mh.convert(file
                                        , schema
                                        , colnames = columns
                                        , row = row
                                        , coltypes = self.cfg_params[KEY_COLUMN_TYPES]
                                        , delimit = self.cfg_params[KEY_DELIMITER])
                    json.dump(result[0], out_file)
                    out_file.write(',')
                out_file.seek(out_file.tell() - 1, os.SEEK_SET)
                out_file.truncate()
                out_file.write(']')

"""
        Main entrypoint
"""
'''
if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug = sys.argv[1]
    else:
        debug = False
    try:
        logging.info("running")
        comp = Component(debug)
        comp.run2()
    except Exception as e:
        logging.exception(e)
        exit(1)
'''

print(__name__)
comp = Component()
comp.run()
