.. django-river documentation master file, created by
   sphinx-quickstart on Sun Aug 30 00:15:25 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |Build Status| image:: https://travis-ci.org/javrasya/django-river.svg
   :target: https://travis-ci.org/javrasya/django-river
.. |Coverage Status| image:: https://coveralls.io/repos/javrasya/django-river/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/javrasya/django-river?branch=master
.. |Health Status| image:: https://landscape.io/github/javrasya/django-river/master/landscape.svg?style=flat
   :target: https://landscape.io/github/javrasya/django-river/master
   :alt: Code Health
.. |Documentation Status| image:: https://readthedocs.org/projects/django-river/badge/?version=latest
   :target: https://readthedocs.org/projects/django-river/?badge=latest
.. |Quality Status| image:: https://api.codacy.com/project/badge/Grade/c3c73d157fe045e6b966d8d4416b6b17
   :alt: Codacy Badge
   :target: https://app.codacy.com/app/javrasya/django-river?utm_source=github.com&utm_medium=referral&utm_content=javrasya/django-river&utm_campaign=Badge_Grade_Dashboard
.. |Logo| image:: https://cloud.githubusercontent.com/assets/1279644/9602162/f198bb06-50ae-11e5-8eef-e9d03ff5f113.png

Django River
============

|Logo|
   
|Build Status| |Coverage Status| |Documentation Status| |Quality Status|

River is an open source and always free workflow framework for ``Django`` which support on
the fly changes instead of hardcoding states, transitions and authorization rules.

The main goal of developing this framework is **to be able to edit any
workflow item on the fly.** This means that all the elements in a workflow like
states, transitions or authorizations rules are editable at any time so that no changes requires a re-deploying of your application anymore.

Getting Started
===============

You can easily get started with ``django-river`` by following :ref:`getting-started`.
    
Contents
========

.. toctree::
   :maxdepth: 2

   getting_started
   overview
   admin/index
   api/index
   authorization
   hooking/index
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

