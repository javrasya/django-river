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
   

.. |Timeline| image:: https://cloud.githubusercontent.com/assets/1279644/9934893/921b543a-5d5c-11e5-9596-a5e067db79ed.png

.. |Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9653471/3c9dfcfa-522c-11e5-85cb-f90a4f184201.png

.. |Closed Without Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9624970/88c0ddaa-515a-11e5-8f65-d1e35e945976.png

.. |Closed With Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9624968/88b5f278-515a-11e5-996b-b62d6e224357.png

.. |Logo| image:: https://cloud.githubusercontent.com/assets/1279644/9602162/f198bb06-50ae-11e5-8eef-e9d03ff5f113.png

Django River
============

|Logo|
   
|Build Status| |Coverage Status| |Documentation Status| |Quality Status|


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
* Django (``1.11``, ``2.0``, ``2.1``, ``2.2``)
* ``Django`` >= 2.0 is supported for ``Python`` >= 3.5


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

3. Create all your ``states`` on the admin page
4. Create a ``workflow`` with your model ( ``MyModel`` - ``my_state_field`` ) information on the admin page
5. Create your ``transition approval metadata`` within the workflow created earlier and authorization rules along with their priority on the admin page
6. Enjoy your ``django-river`` journey.

    .. code-block:: python

        my_model=MyModel.objects.get(....)

        my_model.river.my_state_field.approve(as_user=transactioner_user)
        my_model.river.my_state_field.approve(as_user=transactioner_user, next_state=State.objects.get(label='re-opened'))

        # and much more. Check the documentation

.. note::
    Whenever a model object is saved, it's state field will be initialized with the
    state is given at step-4 above by ``django-river``.

Hooking Up With The Events
--------------------------

`django-river` provides you to have your custom code run on certain events. And since version v2.1.0 this has also been supported for on the fly changes. You can
create your functions and also the hooks to a certain events by just creating few database items. Let's see what event types that can be hooked a function to;

* An approval is approved
* A transition goes through
* The workflow is complete

For all these event types, you can create a hooking with a given function which is created separately and preliminary than the hookings for all the workflow objects you have
or you will possible have, or for a specific workflow object. You can also hook up before or after the events happen.

Create Function
^^^^^^^^^^^^^^^

This will be the description of your functions. So you define them once and you can use them with multiple hooking up. Just go to `/admin/river/function/` admin page
and create your functions there. `django-river` function admin support python code highlights.

   .. code:: python

       INSTALLED_APPS=[
           ...
           codemirror2
           river
           ...
       ]

Here is an example function;

   .. code:: python
        from datetime import datetime

        def handle(context):
            print(datetime.now())
            print(context)

`django-river` will pass a `context` down to your function in respect to in order for you to know why the function is triggered. And the `context` will look different for
different type of events





Contribute
----------

Contributions are welcome! Please join making always totally free ``django-river`` better.

.. _license:

License
=======

This software is licensed under the `New BSD License`. See the ``LICENSE``
file in the top distribution directory for the full license text.
