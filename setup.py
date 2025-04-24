from distutils.core import setup

import setuptools

setup(
    name="csv2json",
    version="0.5.8",
    setup_requires=["setuptools_scm"],
    url="https://github.com/keboola/processor-csv-to-json",
    download_url="https://github.com/keboola/processor-csv-to-json",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=["hone", "strconv"],
    test_suite="tests",
    license="MIT",
)
