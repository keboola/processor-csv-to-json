'''
Template Component main class.

'''

import csv
import glob
import json
import logging
import ntpath
import os
from pathlib import Path
from kbc.env_handler import KBCEnvHandler

from csv2json.hone_csv2json import Csv2JsonConverter

# #### Keep for debug
KEY_DELIMITER = 'delimiter'
KEY_COLUMN_TYPES = 'column_types'
KEY_INFER = 'infer_undefined'
KEY_NAMES_OVERRIDE= 'column_names_override'
MANDATORY_PARS = [KEY_DELIMITER]

APP_VERSION = '0.0.1'


class Component(KBCEnvHandler):
    def __init__(self):
        # for easier local project setup
        default_data_dir = Path(__file__).resolve().parent.parent.joinpath('data').as_posix() \
            if not os.environ.get('KBC_DATADIR') else None

        KBCEnvHandler.__init__(self, MANDATORY_PARS, data_path=default_data_dir)
        self.validate_config(MANDATORY_PARS)
        self.delimiter = self.cfg_params[KEY_DELIMITER]
        self.column_types = self.cfg_params.get(KEY_COLUMN_TYPES, None)

        self.input_tables = glob.glob(self.tables_in_path + "/*[!.manifest]")

        self.set_default_logger(logging.INFO)

        logging.info('Loading configuration...')

    def run(self):
        for file in self.input_tables:
            logging.info("Processing table %s" % file)

            # if not self.column_types
            # returns nested JSON schema for input.csv
            os.makedirs(self.files_out_path, exist_ok=True)
            os.makedirs(self.tables_out_path, exist_ok=True)
            with open(file, mode='rt', encoding='utf-8') as in_file, \
                    open(os.path.join(self.files_out_path,
                                      ntpath.basename(file).replace('.csv', '')) + '.json',
                         mode='wt', encoding='utf-8') as out_file:
                reader = csv.reader(in_file, lineterminator='\n')
                out_file.write('[')
                header = next(reader, None)
                mh = Csv2JsonConverter(header, delimiter=self.delimiter)
                for row in reader:
                    result = mh.convert_row(row=row,
                                            coltypes=self.cfg_params[KEY_COLUMN_TYPES],
                                            colname_override=self.cfg_params.get(KEY_NAMES_OVERRIDE),
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
if __name__ == "__main__":
    try:
        comp = Component()
        comp.run()
    except Exception as exc:
        logging.exception(exc)
        exit(1)
