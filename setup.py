__author__ = 'ahmetdal'

from setuptools import setup, find_packages

try:
    long_description = open('README.md').read()
except IOError:
    long_description = ''

setup(
    name='django-river',
    version='0.3.1',
    author='Ahmet DAL',
    author_email='ceahmetdal@gmail.com',
    packages=find_packages(),
    url='https://github.com/javrasya/django-river.git',
    description='Django Workflow Library',
    long_description=long_description,
    dependency_links=[
        "https://bitbucket.org/ahmetdal/river.io-python/tarball/master/#egg=0.0.1"
    ],
    install_requires=[
        "Django",
        "mock",
        "factory-boy"
    ],
    include_package_data=True,
    zip_safe=False,
    license='GPLv3',
    platforms=['any'],
)
