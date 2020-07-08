'''
Created on 12. 11. 2018

@author: esner
'''
import mock
import unittest
from freezegun import freeze_time
import sys
import os

sys.path.append(os.getcwd() + "/src")
from component import Component
import filecmp

KBC_DATADIR = os.environ.get('KBC_DATADIR')
KBC_TESTDIR = os.environ.get('KBC_TESTDIR')


class TestComponent(unittest.TestCase):

    # set global time to 2010-10-10 - affects functions like datetime.now()
    @freeze_time("2010-10-10")
    # set KBC_DATADIR env to non-existing dir
    @mock.patch.dict(os.environ, {'KBC_DATADIR': './non-existing-dir'})
    def test_run_no_cfg_fails(self):
        with self.assertRaises(ValueError):
            comp = Component()
            comp.run()

    def test_structure(self):
        '''
        tests if the resulting hierarchy of files conforms to the specififed one
        '''
        for test in os.listdir(f'{KBC_TESTDIR}/functional'):
            if test.startswith('.'):
                continue
            os.environ["KBC_DATADIR"] = f'{KBC_TESTDIR}/functional/{test}/source/data'
            with self.assertRaises(AssertionError,
                                   msg=f'The result structure is not what was expected!'):
                comp = Component()
                comp.run()
                a = self.compare_output_structure(test)
                assert 0 != self.compare_output_structure(test)

    def compare_output_structure(self, test_name):
        '''
        compares the expected output files/tables with the actual output files
        '''
        out_files_expected = [file for file in
                              os.listdir(KBC_TESTDIR + f'/functional/{test_name}/expected/data/out/files') if
                              not file.startswith('.')]
        out_tables_expected = [file for file in
                               os.listdir(KBC_TESTDIR + f'/functional/{test_name}/expected/data/out/tables') if
                               not file.startswith('.')]
        out_files_real = [file for file in os.listdir(KBC_TESTDIR + f'/functional/{test_name}/source/data/out/files') if
                          not file.startswith('.')]
        out_tables_real = [file for file in os.listdir(KBC_TESTDIR + f'/functional/{test_name}/source/data/out/tables')
                           if not file.startswith('.')]

        if set(out_files_real) != set(out_files_expected) or set(out_tables_real) != set(out_tables_expected):
            return 1

        for file_real in out_files_real:
            for file_expected in out_files_expected:
                if file_real == file_expected:
                    is_the_same = filecmp.cmp(KBC_TESTDIR + f'/functional/{test_name}/source/data/out/files/{file_real}',
                                KBC_TESTDIR + f'/functional/{test_name}/expected/data/out/files/{file_expected}')
                    if not is_the_same:
                        return 1

        for table_real in out_tables_real:
            for table_expected in out_tables_expected:
                if table_real == table_expected:
                    is_the_same = filecmp.cmp(KBC_TESTDIR + f'/functional/{test_name}/source/data/out/files/{table_real}',
                                KBC_TESTDIR + f'/functional/{test_name}/expected/data/out/files/{table_expected}')
                    if not is_the_same:
                        return 1

        return 0


if __name__ == "__main__":
    unittest.main()
