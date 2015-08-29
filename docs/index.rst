.. django-river documentation master file, created by
   sphinx-quickstart on Sun Aug 30 00:15:25 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

django-river - Workflow Library for Django!
===========================================

.. image:: https://travis-ci.org/javrasya/django-river.svg?branch=0.3.1
    :target: https://travis-ci.org/javrasya/django-river

.. image:: https://coveralls.io/repos/javrasya/django-river/badge.svg?branch=0.3.1&service=github
  :target: https://coveralls.io/github/javrasya/django-river?branch=0.3.1

``django-river`` is a open source workflow system for ``Django`` which support on the fly changes on every item in workflow instead of hardcoding states and transitions.

Main goal of developing this framework is **to be able to edit any workflow item on the fly.** This means, all elements in workflow like states, transitions, user authorizations(permission), group authorization are editable. To do this, all data about the workflow item is persisted into DB. **Hence, they can be changed without touching the code and re-deploying your application.**

There is ordering aprovments for a transition functionality in ``django-river``. It also provides skipping specific transition of a specific objects.


Contents:

.. toctree::
   :maxdepth: 2

   overview
   installation
   configuration
   guide/developer/index
   guide/end-user/index



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

