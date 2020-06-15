from distutils.core import setup

import setuptools

setup(
    name='csv2json',
    version='0.1.5',
    setup_requires=['setuptools_scm'],
    url='https://bitbucket.org/kds_consulting_team/kds-team.processor-csv-to-json',
    download_url='https://bitbucket.org/kds_consulting_team/kds-team.processor-csv-to-json',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=[
        'hone'
    ],
    test_suite='tests',
    license="MIT"
)
