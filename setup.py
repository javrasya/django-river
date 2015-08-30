__author__ = 'ahmetdal'

from setuptools import setup, find_packages

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='django-river',
    version='0.3.2',
    author='Ahmet DAL',
    author_email='ceahmetdal@gmail.com',
    packages=find_packages(),
    url='https://github.com/javrasya/django-river.git',
    description='Django Workflow Library',
    long_description=read_md('README.md'),
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
