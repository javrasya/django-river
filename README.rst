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

.. |Downloads| image:: https://img.shields.io/pypi/dm/django-river
    :alt: PyPI - Downloads

.. |Discord| image:: https://img.shields.io/discord/651433240019599400
    :target: https://discord.gg/DweUwZX
    :alt: Discord

.. |Open Collective| image:: https://opencollective.com/django-river/all/badge.svg?label=financial+contributors
    :alt: Financial Contributors
    :target: #contributors

.. |Timeline| image:: https://cloud.githubusercontent.com/assets/1279644/9934893/921b543a-5d5c-11e5-9596-a5e067db79ed.png

.. |Logo| image:: docs/logo.svg
    :width: 200

.. |Create Function Page| image:: docs/_static/create-function.png

Django River
============

|Logo|

|Build Status| |Coverage Status| |Documentation Status| |Quality Status| |Downloads| |Discord|

River is an open source workflow framework for ``Django`` which supports on
the fly changes instead of hard-coding states, transitions and authorization rules.

The main goal of developing this framework is **to be able to modify literally everything
about the workflows on the fly.** This means that all the elements in a workflow like
states, transitions or authorizations rules are editable at any time so that no changes
requires a re-deploying of your application anymore.

**Playground**: There is a fake jira example repository as a playground of django-river. https://github.com/javrasya/fakejira

Donations
---------

This is a fully open source project and it can be better with your donations.

If you are using ``django-river`` to create a commercial product,
please consider becoming our `sponsor`_  , `patron`_ or donate over `PayPal`_

.. _`patron`: https://www.patreon.com/javrasya
.. _`PayPal`: https://paypal.me/ceahmetdal
.. _`sponsor`: https://github.com/sponsors/javrasya

Documentation
-------------

Online documentation is available at http://django-river.rtfd.org/

Advance Admin
-------------

A very modern admin with some user friendly interfaces that is called `River Admin`_ has been published.

.. _`River Admin`: https://riveradminproject.com/

Requirements
------------
* Python (``3.5`` (for Django ``2.2`` only), ``3.6``, ``3.7``, ``3.8``)
* Django (``2.2``, ``3.0``, ``3.1``)
* ``Django`` = 2.2 is supported for ``Python`` >= 3.5
* ``Django`` >= 3.0 is supported for ``Python`` >= 3.6

Supported (Tested) Databases:
-----------------------------

+------------+--------+---------+
| PostgreSQL | Tested | Support |
+------------+--------+---------+
| 9          |   ✅   |    ✅   |
+------------+--------+---------+
| 10         |   ✅   |    ✅   |
+------------+--------+---------+
| 11         |   ✅   |    ✅   |
+------------+--------+---------+
| 12         |   ✅   |    ✅   |
+------------+--------+---------+

+------------+--------+---------+
| MySQL      | Tested | Support |
+------------+--------+---------+
| 5.6        |   ✅   |    ❌   |
+------------+--------+---------+
| 5.7        |   ✅   |    ❌   |
+------------+--------+---------+
| 8.0        |   ✅   |    ✅   |
+------------+--------+---------+

+------------+--------+---------+
| MSSQL      | Tested | Support |
+------------+--------+---------+
| 19         |   ✅   |    ✅   |
+------------+--------+---------+
| 17         |   ✅   |    ✅   |
+------------+--------+---------+


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
5. Create your ``transition metadata`` within the workflow created earlier, source and destination states
6. Create your ``transition approval metadata`` within the workflow created earlier and authorization rules along with their priority on the admin page
7. Enjoy your ``django-river`` journey.

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

1. Create Function
^^^^^^^^^^^^^^^^^^

This will be the description of your functions. So you define them once and you can use them with multiple hooking up. Just go to ``/admin/river/function/`` admin page
and create your functions there. ``django-river`` function admin support python code highlights.

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

**Important:** **YOUR FUNCTION SHOULD BE NAMED AS** ``handle``. Otherwise ``django-river`` won't execute your function.

``django-river`` will pass a ``context`` down to your function in order for you to know why the function is triggered or for which object or so. And the ``context`` will look different for
different type of events. Please see detailed `context documentation`_ to know more on what you would get from context in your functions.

You can find an `advance function example`_ on the link.

|Create Function Page|

.. _`context documentation`: https://django-river.readthedocs.io/en/latest/hooking/function.html#context-parameter
.. _`advance function example`: https://django-river.readthedocs.io/en/latest/hooking/function.html#example-function

2. Hook It Up
^^^^^^^^^^^^^

The hookings in ``django-river`` can be created both specifically for a workflow object or for a whole workflow. ``django-river`` comes with some model objects and admin interfaces which you can use
to create the hooks.

* To create one for whole workflow regardless of what the workflow object is, go to

    * ``/admin/river/onapprovedhook/`` to hook up to an approval
    * ``/admin/river/ontransithook/`` to hook up to a transition
    * ``/admin/river/oncompletehook/`` to hook up to the completion of the workflow

* To create one for a specific workflow object you should use the admin interface for the workflow object itself. One amazing feature of ``django-river`` is now that it creates a default admin interface with the hookings for your workflow model class. If you have already defined one, ``django-river`` enriches your already defined admin with the hooking section. It is default disabled. To enable it just define ``RIVER_INJECT_MODEL_ADMIN`` to be ``True`` in the ``settings.py``.


**Note:** They can programmatically be created as well since they are model objects. If it is needed to be at workflow level, just don't provide the workflow object column. If it is needed
to be for a specific workflow object then provide it.

Here are the list of hook models;

* OnApprovedHook
* OnTransitHook
* OnCompleteHook

Before Reporting A Bug
----------------------

``django-river`` has behavioral tests that are very easy to read and write. One can easily set up one
and see if everything is running as expected. Please look at other examples (that are the files with ``.feature`` postfix)
under ``features`` folder that you can get all the inspiration and create one for yourself before you open an issue
Then refer to your behavioral test to point out what is not function as expected to speed the process up for your own
sake. It is even better to name it with your issue number so we can persist it in the repository.

Migrations
----------

2.X.X to 3.0.0
^^^^^^^^^^^^^^

``django-river`` v3.0.0 comes with quite number of migrations, but the good news is that even though those are hard to determine kind of migrations, it comes with the required migrations
out of the box. All you need to do is to run;


   .. code:: bash

       python manage.py migrate river

3.1.X to 3.2.X
^^^^^^^^^^^^^^

``django-river`` started to support **Microsoft SQL Server 17 and 19** after version 3.2.0 but the previous migrations didn't get along with it. We needed to reset all
the migrations to have fresh start. If you have already migrated to version `3.1.X` all you need to do is to pull your migrations back to the beginning.


   .. code:: bash

       python manage.py migrate --fake river zero
       python manage.py migrate --fake river

FAQ
---

Have a look at `FAQ`_

.. _`FAQ`: https://django-river.readthedocs.io/en/latest/faq.html

Contributors
============

Code Contributors
------------------

This project exists thanks to all the people who contribute :rocket: :heart:

.. image:: https://opencollective.com/django-river/contributors.svg?width=890&button=false
    :target: https://github.com/javrasya/django-river/graphs/contributors

Financial Contributors
----------------------

Become a financial contributor and help us sustain our community. Contribute_

Individuals
^^^^^^^^^^^

.. image:: https://opencollective.com/django-river/individuals.svg?width=890
    :target: https://opencollective.com/django-river

Organizations
^^^^^^^^^^^^^

Support this project with your organization. Your logo will show up here with a link to your website. Contribute_

.. image:: https://opencollective.com/django-river/organization/0/avatar.svg
    :target: https://opencollective.com/django-river/organization/0/website

.. _Contribute: https://opencollective.com/django-river

.. _license:

License
=======

This software is licensed under the `New BSD License`. See the ``LICENSE``
file in the top distribution directory for the full license text.
