'''
Created on 12. 11. 2018

@author: esner
'''
import os
import unittest
from os import path
from os.path import dirname

from component import Component

FUNCTIONAL_TEST_DIR = path.join(dirname(path.realpath(__file__)), 'functional')


class TestFunctional(unittest.TestCase):

    def test_functional(self):
        '''
        tests if the resulting hierarchy of files conforms to the specififed one
        '''
        os.path.dirname(os.path.realpath(__file__))
        test_errors = []
        for test in os.listdir(FUNCTIONAL_TEST_DIR):
            if test.startswith('.'):
                continue
            test_dir = path.join(FUNCTIONAL_TEST_DIR, test)
            data_dir = path.join(test_dir, 'source', 'data')
            os.environ["KBC_DATADIR"] = data_dir
            comp = Component()
            comp.run()
            result = self.compare_output_structure(test, test_dir)
            if result:
                test_errors.append(f'Functional test {test} failed with error: {result}!')

        self.assertEqual(test_errors, [], msg=', \n '.join(test_errors))

    def compare_output_structure(self, test_name, test_dir):
        '''
        compares the expected output files/tables with the actual output files
        '''
        out_files_expected = [file for file in
                              os.listdir(path.join(test_dir, 'expected', 'data', 'out', 'files')) if
                              not file.startswith('.')]
        out_tables_expected = [file for file in
                               os.listdir(path.join(test_dir, 'expected', 'data', 'out', 'tables')) if
                               not file.startswith('.')]
        out_files_real = [file for file in os.listdir(path.join(test_dir, 'source', 'data', 'out', 'files')) if
                          not file.startswith('.')]
        out_tables_real = [file for file in os.listdir(path.join(test_dir, 'source', 'data', 'out', 'tables'))
                           if not file.startswith('.')]

        if set(out_files_real) == set(out_files_expected) and set(out_tables_real) == set(out_tables_expected):
            return 0
        else:
            return 1


if __name__ == "__main__":
    unittest.main()
