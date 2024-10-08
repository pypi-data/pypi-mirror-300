import re
import os
from distutils.command.register import register as register_orig
from distutils.command.upload import upload as upload_orig
from setuptools import setup,find_packages

# Read version from file without loading the module
with open('src/RainyLibrary/version.py', 'r') as version_file:
    version_match = re.search(r"^VERSION ?= ?['\"]([^'\"]*)['\"]", version_file.read(), re.M)
if version_match:
    VERSION=version_match.group(1)
else:
    VERSION='0.1'

requirements = [
    'robotframework==7.1',
    'robotframework-browsermobproxylibrary==0.1.3',
    'robotframework-browser',
    'robotframework-debuglibrary',
    'robotframework-databaselibrary',
    'robotframework-datadriver',
    'robotframework-datetime-tz',
    'robotframework-faker',
    'robotframework-seleniumlibrary',
    'robotframework-seleniumtestability',
    'robotframework-pdf2textlibrary',
    'robotframework-pabot',
    'robotframework-requests',
    'robotframework-sshlibrary',
    'robotframework-robocop',
    'robotframework-jsonlibrary',
    'robotframework-imaplibrary2',
    'robotframework-excellib',
    'robotframework-appiumlibrary',
    'robotframework-csvlibrary',
    'RESTinstance',
    'jsonpath2',
    'pyzxing',
    'PyMySQL',
    'PyYAML',
    'DateTime',
    'openpyxl',
    'certifi',
    'cx-Oracle',
    'opencv-python',
    'PyPDF2'
]

test_requirements = [
    # TODO: put package test requirements here
]


CLASSIFIERS = """
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Framework :: Robot Framework
Framework :: Robot Framework :: Library
"""[1:-1]


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='robotframework-RainyLibrary',
    version=VERSION,
    description="rainy common library for robot framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="watchagorn pattummee",
    author_email='wpchagorn24@gmail.com',
    url='https://gitlab.com/wpchagorn24/robotframework-rainylibrary',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='RainyWebCommon, RainyCommon, RainyAppCommon,RainyLibrary',
    classifiers=CLASSIFIERS.splitlines(),
    test_suite='tests',
    tests_require=test_requirements
)