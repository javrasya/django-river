import os
import sys

__author__ = 'ahmetdal'

from setuptools import setup, find_packages

readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
try:
    long_description = open(readme_file).read()
except IOError as err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
                     "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

setup(
    name='django-river',
    version='0.8.0',
    author='Ahmet DAL',
    author_email='ceahmetdal@gmail.com',
    packages=find_packages(),
    url='https://github.com/javrasya/django-river.git',
    description='Django Workflow Library',
    long_description=long_description,
    install_requires=[
        "Django",
        "mock",
        "factory-boy",
        "django-mptt"
    ],
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    platforms=['any'],
)
