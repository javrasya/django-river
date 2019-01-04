.. |Build Status| image:: https://travis-ci.org/javrasya/django-river.svg
    :target: https://travis-ci.org/javrasya/django-river
.. |Coverage Status| image:: https://coveralls.io/repos/javrasya/django-river/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/javrasya/django-river?branch=master

.. |Health Status| image:: https://landscape.io/github/javrasya/django-river/master/landscape.svg?style=flat
    :target: https://landscape.io/github/javrasya/django-river/master
   :alt: Code Health

.. |Documentation Status| image:: https://readthedocs.org/projects/django-river/badge/?version=latest
    :target: https://readthedocs.org/projects/django-river/?badge=latest

.. |Timeline| image:: https://cloud.githubusercontent.com/assets/1279644/9934893/921b543a-5d5c-11e5-9596-a5e067db79ed.png

.. |Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9653471/3c9dfcfa-522c-11e5-85cb-f90a4f184201.png

.. |Closed Without Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9624970/88c0ddaa-515a-11e5-8f65-d1e35e945976.png

.. |Closed With Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9624968/88b5f278-515a-11e5-996b-b62d6e224357.png

.. |Logo| image:: https://cloud.githubusercontent.com/assets/1279644/9602162/f198bb06-50ae-11e5-8eef-e9d03ff5f113.png

Django River
============

|Logo|
   
|Build Status| |Coverage Status| |Health Status| |Documentation Status|


Contributors are welcome. Come and give a hand :-)
---------------------------------------------------

River is an open source workflow framework for ``Django`` which support on
the fly changes instead of hardcoding states, transitions and authorization rules.

The main goal of developing this framework is **to be able to edit any
workflow item on the fly.** This means that all the elements in a workflow like
states, transitions or authorizations rules are editable at any time so that no changes requires a re-deploying of your application anymore.

**Playground**: There is a fake jira example repository as a playground of django-river. https://github.com/javrasya/fakejira

Documentation
-------------

Online documentation is available at http://django-river.rtfd.org/.

Requirements
------------
* Python (``2.7``, ``3.4``, ``3.5``, ``3.6``)
* Django (``1.7``, ``1.8``, ``1.9``, ``1.10``, ``1.11``, ``2.0``, ``2.1``)
* ``Django`` >= 2.0 is supported for ``Python`` >= 3.5
* ``Django`` == 1.7 is only supported for ``Python`` == 2.7 and ``Python`` == 3.4


Usage
-----
1. Install and enable it

   .. code:: bash

       pip install django-river


   .. code:: python

       INSTALLED_APPS=[
       ...
       river
       ...
       ]

2. Create your first state machine in your model and migrate your db

    .. code:: python

        from django.db import models
        from river.models.fields.state import StateField

        class MyModel(models.Model):
            my_state_field = StateField()

3. Create your states as one of them will be your initial state on the admin page
4. Create your transition approval metadata with your model (``MyModel`` - ``my_state_field``) information and authorization rules along with their priority on the admin page
5. Enjoy your ``django-river`` journey.

    .. code-block:: python

        my_model=MyModel.objects.get(....)

        my_model.river.my_state_field.approve(as_user=transactioner_user)
        my_model.river.my_state_field.approve(as_user=transactioner_user,next_state=State.objects.get(label='re-opened'))

        # and much more. Check the documentation

.. note::
    Whenever a model object is saved, it's state field will be initialized with the
    state is given at step-3 above by ``django-river``.

.. note::
    Make sure that there is only one initial state defined in your workflow, so that ``django-river`` can pick that one automatically
    when a model object is created. All other workflow items will be managed by ``django-river`` after object creations.



Example Scenarios
-----------------
Simple Issue Tracking System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Re-Open case
""""""""""""
|Re Open Case|

Closed without Re-Open case
"""""""""""""""""""""""""""
|Closed Without Re Open Case|

Closed with Re-Open case
""""""""""""""""""""""""
|Closed With Re Open Case|

Contribute
----------

Contributions are welcome! Please join making always totally free ``django-river`` better.