'''
Template Component main class.

'''

import csv
import glob
import json
import logging
import ntpath
import os

from kbc.env_handler import KBCEnvHandler

from csv2json.hone_csv2json import Csv2JsonConverter

# #### Keep for debug
KEY_DELIMITER = 'delimiter'
KEY_COLUMN_TYPES = 'column_types'
KEY_INFER = 'infer_undefined'
MANDATORY_PARS = [KEY_DELIMITER]

APP_VERSION = '0.0.1'


class Component(KBCEnvHandler):
    def __init__(self):
        KBCEnvHandler.__init__(self, MANDATORY_PARS)
        self.validate_config(MANDATORY_PARS)
        self.delimiter = self.cfg_params[KEY_DELIMITER]
        self.column_types = self.cfg_params.get(KEY_COLUMN_TYPES, None)

        self.input_tables = glob.glob(self.tables_in_path + "/*[!.manifest]")

        self.set_default_logger(logging.INFO)

        logging.info('Loading configuration...')

    def run(self):
        for file in self.input_tables:
            logging.info("Processing table %s" % file)
            mh = Csv2JsonConverter(csv_file_path=file, delimiter=self.delimiter)
            # if not self.column_types
            # returns nested JSON schema for input.csv
            with open(file, mode='rt', encoding='utf-8') as in_file, \
                    open(os.path.join(self.data_path, 'out', "files",
                                      ntpath.basename(file).replace('.csv', '')) + '.json',
                         mode='wt', encoding='utf-8') as out_file:
                reader = csv.reader(in_file, lineterminator='\n')
                out_file.write('[')
                next(reader, None)
                for row in reader:
                    result = mh.convert_row(row=row,
                                            coltypes=self.cfg_params[KEY_COLUMN_TYPES],
                                            delimit=self.cfg_params[KEY_DELIMITER],
                                            infer_undefined=self.cfg_params.get(KEY_INFER, False))
                    json.dump(result[0], out_file)
                    out_file.write(',')
                logging.info("All rows have been processed.")
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
