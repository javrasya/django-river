.. |Build Status| image:: https://travis-ci.org/javrasya/django-river.svg
   :target: https://travis-ci.org/javrasya/django-river
.. |Coverage Status| image:: https://coveralls.io/repos/javrasya/django-river/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/javrasya/django-river?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/django-river/badge/?version=latest
   :target: https://readthedocs.org/projects/django-river/?badge=latest

Django River
============

.. image:: https://cloud.githubusercontent.com/assets/1279644/9602162/f198bb06-50ae-11e5-8eef-e9d03ff5f113.png

|Build Status| |Coverage Status| |Documentation Status|

River is a open source workflow system for ``Django`` which support on
the fly changes on every item in workflow instead of hardcoding states
and transitions.

Main goal of developing this framework is **to be able to edit any
workflow item on the fly.** This means, all elements in workflow like
states, transitions, user authorizations(permission), group
authorization are editable. To do this, all data about the workflow item
is persisted into DB. **Hence, they can be changed without touching the
code and re-deploying your application.**

There is ordering aprovments for a transition functionality in
``django-river``. It also provides skipping specific transition of a
specific objects.

Documentation
-------------

Online documentation is available at http://django-river.rtfd.org/.

Requirements
------------
* Python (``2.7``, ``3.2``, ``3.3``, ``3.4``)
* Pypy (``2``, ``3``)
* Django (``1.7``, ``1.8``)

Installation
------------

-  Install it

   .. code:: bash

       pip install django-river

-  Configure settings

   .. code:: python

       INSTALLED_APPS=[
       ...
       river
       ...
       ]

-  Migrate your application

   .. code:: bash

       python manage.py migrate

-  In your model class which will be processing in workflow;

.. code:: python

    from django.db import models
    from river.models.fields.state import StateField

    class MyModel(models.Model):
        my_state_field = StateField()

.. code-block:: python

    my_model=MyModel.objects.get(....)
    
    my_model.proceed(transactioner_user)
    my_model.proceed(transactioner_user,next_state=State.objects.get(label='re-opened'))


That's it. Whenever your new model object is saved, it's state field
will be initialized according to given meta data about workflow. ``proceed`` methods is injected into your model objects. The object will be in next state if the given user is authorized to do that transaction. When there is two destination states available from current state, ``next_state`` must be given to the function. If there is only one state can be at, no needs to give it; ``django-river`` will detect it.

Usage for End User
------------------

1. Define your states.
2. Define your state transitions.
3. Define your proceeding metas which contains permissions and groups
   authorization for transitions. Proceeding order is also given here.

.. note::
   There must be only one initial state candidate for your workflow scenarios. Because ``django-river`` is gonna try to detect it and initialize your objects workflow path. If there are more than one initial state, ``django-river`` will raise ``RiverException(error_code=3)`` which is ``MULTIPLE_INITIAL_STATE`` error.


Whenever an object of MyModel is inserted in your system, all its
workflow initialization is done by ``django-river``.

Usage for Developer
-------------------

Signals:
~~~~~~~~

``pre_transition``: it is fired before any transition occured.

+-------------------+---------------------------------------+
| Args              | Description                           |
+===================+=======================================+
| workflow_object   | Your object on transition             |
+-------------------+---------------------------------------+
| field             | Field which you registered object for |
+-------------------+---------------------------------------+
| source_state      | Transition source state object        |
+-------------------+---------------------------------------+
| destination_state | Transition destination state object   |
+-------------------+---------------------------------------+
| proceeding        | Proceeding object                     |
+-------------------+---------------------------------------+

``post_transition``: it is fired before any transition occured.

+-------------------+---------------------------------------+
| Args              | Description                           |
+===================+=======================================+
| workflow_object   | Your object on transition             |
+-------------------+---------------------------------------+
| field             | Field which you registered object for |
+-------------------+---------------------------------------+
| source_state      | Transition source state object        |
+-------------------+---------------------------------------+
| destination_state | Transition destination state object   |
+-------------------+---------------------------------------+
| proceeding        | Proceeding object                     |
+-------------------+---------------------------------------+

``pre_proceed``: it is fired before any is proceeded. Transition
does not have to be occured.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object proceeded                 |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+
| proceeding      | Proceeding object                     |
+-----------------+---------------------------------------+
| track           | Proceeding track object               |
+-----------------+---------------------------------------+

``post_proceed``: it is fired before any is proceeded occured.
Transition does not have to be occured.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object proceeded                 |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+
| proceeding      | Proceeding object                     |
+-----------------+---------------------------------------+
| track           | Proceeding track object               |
+-----------------+---------------------------------------+

``pre_final``: it is fired before any workflow is completed.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object on final                  |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+

``post_final``: it is fired before any workflow is completed.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object on final                  |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+

Handlers:
---------

Handlers are different from ``django-river`` signals. These are for
spesific object, spesific source_state, spesific destination_state
etc. It is fired when the condition is matched.

PreCompletedHandler:
~~~~~~~~~~~~~~~~~~~~


Before an object is on final state, if the condition is match; means
object is suitable, it is fired;

.. code:: python

    from river.handlers.completed import PreCompletedHandler

    def handler(my_object,field,*args,**kwargs):
        do_something_with(object,field)

    PreCompletedHandler.register(handler,my_object,'my_state_field')

``register`` method parameter

+-----------------+---------------------------------------+----------+
| Args            | Description                           |          |
+=================+=======================================+==========+
| workflow_object | Your object proceeded                 | Required |
+-----------------+---------------------------------------+----------+
| field           | Field which you registered object for | Required |
+-----------------+---------------------------------------+----------+

PostCompletedHandler:
~~~~~~~~~~~~~~~~~~~~~

After an object is on final state, if the condition is match; means
object is suitable, it is fired;

.. code:: python

    from river.handlers.completed import PostCompletedHandler

    def handler(my_object,field,*args,**kwargs):
        do_something_with(object,field)

    PostCompletedHandler.register(handler,my_object,'my_state_field')

``register`` method parameter

+-----------------+---------------------------------------+----------+
| Args            | Description                           |          |
+=================+=======================================+==========+
| workflow_object | Your object proceeded                 | Required |
+-----------------+---------------------------------------+----------+
| field           | Field which you registered object for | Required |
+-----------------+---------------------------------------+----------+

PreTransitionHandler:
~~~~~~~~~~~~~~~~~~~~~

Before any transition occurred, if the condition is match; means object,
source_state,destination state are suitable, it is fired;

.. code:: python

    from river.handlers.transition import PreTransitionHandler

    def handler(my_object,field,*args,**kwargs):
        do_something_with(object,field)

    PreTransitionHandler.register(handler,my_object,'my_state_field')

``register`` method parameter

+------------------+---------------------------------------+----------+
| Args             | Description                           |          |
+==================+=======================================+==========+
| workflow_object  | Your object proceeded                 | Required |
+------------------+---------------------------------------+----------+
| field            | Field which you registered object for | Required |
+------------------+---------------------------------------+----------+
| source_state     | Source state of the tranition         | Optional |
+------------------+---------------------------------------+----------+
| desination_satte | Destinatio state of the tranition     | Optional |
+------------------+---------------------------------------+----------+

PostTransitionHandler:
~~~~~~~~~~~~~~~~~~~~~~

After any transition occurred, if the condition is match; means object,
source_state,destination state are suitable, it is fired;

.. code:: python

    from river.handlers.transition import PostTransitionHandler

    def handler(my_object,field,*args,**kwargs):
        do_something_with(object,field)

    PostTransitionHandler.register(handler,my_object,'my_state_field')

``register`` method parameter

+------------------+---------------------------------------+----------+
| Args             | Description                           |          |
+==================+=======================================+==========+
| workflow_object  | Your object   proceeded               | Required |
+------------------+---------------------------------------+----------+
| field            | Field which you registered object for | Required |
+------------------+---------------------------------------+----------+
| source_state     | Source state of the tranition         | Optional |
+------------------+---------------------------------------+----------+
| desination_satte | Destinatio state of the tranition     | Optional |
+------------------+---------------------------------------+----------+

Handler Backends:
-----------------
Handlers can be persisted into different sources. This functionality is added for multiprocessing. Now, backends supports multiprocessing can be implemented.

+----------------------------+-----------------+-------------------------------------------------------------+
| Backend                    | Multiprocessing | Path                                                        |
+============================+=================+=============================================================+
| ``MemoryHandlerBackend``   | No              | ``river.handlers.backends.memory.MemoryHandlerBackend``     |
+----------------------------+-----------------+-------------------------------------------------------------+
| ``DatabaseHandlerBackend`` | Yes             | ``river.handlers.backends.database.DatabaseHandlerBackend`` |
+----------------------------+-----------------+-------------------------------------------------------------+

Default backend is ``MemoryHandlerBackend`` which does not supports multiprocessing. It can be updated in settings file;

.. code-block:: python

    RIVER_HANDLER_BACKEND = {
        'backend':'river.handlers.backends.database.DatabaseHandlerBackend'
    }


Models:
-------

States:
~~~~~~~

Indicates states in your state machine.

Transitions:
~~~~~~~~~~~~

These are transition between your states. **There must be only one
initial state** which is in a transition as destination state but no
source state to make ``django-river`` find it on object creation.

Proceeding Meta:
~~~~~~~~~~~~~~~~~

These are proceeding meta of transitions that describes which user
permission or user group will be allowed to proceed the transition.
These are kind of template for proceedings will be created for each
object. An order can also be given here for the transition. This means,
If you want to order proceeding for a transition, you can define it.
Assume **s1** and **s2** are our states and there is a transition
defined between them and we have two proceeding meta on this
transition. They shall be for\ **permission1** and **permission2**. If
you want object available for proceeding; first **permission1** and after it is
proceeded by permission1, then it is on approval the second permission
which is **permission2**, you can do it with ``djang-river`` by defining
order in this model.

Proceeding:
~~~~~~~~~~~~

There are state machines paths which is needed to be proceeded for every
particular object. Proceedings are generated on your model object
creation by using ``proceeding meta``. This is whole path for the
created object. Do not add or edit this model data unless you don't need
specific objects editing like skiping, overriding permissions and
groups.



.. image:: https://d2weczhvl823v0.cloudfront.net/javrasya/django-river/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

