.. |Build Status| image:: https://travis-ci.org/javrasya/django-river.svg
    :target: https://travis-ci.org/javrasya/django-river
.. |Coverage Status| image:: https://coveralls.io/repos/javrasya/django-river/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/javrasya/django-river?branch=master

.. |Health Status| image:: https://landscape.io/github/javrasya/django-river/master/landscape.svg?style=flat
    :target: https://landscape.io/github/javrasya/django-river/master
   :alt: Code Health

.. |Documentation Status| image:: https://readthedocs.org/projects/django-river/badge/?version=latest
    :target: https://readthedocs.org/projects/django-river/?badge=latest
.. |SimpleJiraExample| image:: http://img.youtube.com/vi/5EZGnTf39aI/0.jpg
    :alt: Simple jira example
   :target: https://www.youtube.com/watch?v=5EZGnTf39aI

.. |Timeline| image:: https://cloud.githubusercontent.com/assets/1279644/9934893/921b543a-5d5c-11e5-9596-a5e067db79ed.png

.. |Gitter| image:: https://badges.gitter.im/Join%20Chat.svg
    :alt: Join the chat at https://gitter.im/javrasya/django-river
   :target: https://gitter.im/javrasya/django-river?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

.. |Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9653471/3c9dfcfa-522c-11e5-85cb-f90a4f184201.png

.. |Closed Without Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9624970/88c0ddaa-515a-11e5-8f65-d1e35e945976.png

.. |Closed With Re Open Case| image:: https://cloud.githubusercontent.com/assets/1279644/9624968/88b5f278-515a-11e5-996b-b62d6e224357.png


Django River
============

.. image:: https://cloud.githubusercontent.com/assets/1279644/9602162/f198bb06-50ae-11e5-8eef-e9d03ff5f113.png

|Build Status| |Coverage Status| |Health Status| |Documentation Status| |Gitter|

River is a open source workflow system for ``Django`` which support on
the fly changes on every item in workflow instead of hardcoding states
and transitions.

Main goal of developing this framework is **to be able to edit any
workflow item on the fly.** This means, all elements in workflow like
states, transitions, user authorizations(permission), group
authorization are editable. To do this, all data about the workflow item
is persisted into DB. **Hence, they can be changed without touching the
code and re-deploying your application.**

There are lining up approvements functionality for a transition in
``django-river``. It also provides skipping specific transition of a
specific objects.

**Playground**: There is a fake jira example repository as a playground of django-river. https://github.com/javrasya/fakejira

Documentation
-------------

Online documentation is available at http://django-river.rtfd.org/.

Video Tutorials
---------------

Simple Jira Example
^^^^^^^^^^^^^^^^^^^

|SimpleJiraExample|


Requirements
------------
* Python (``2.7``, ``3.4``, ``3.5``, ``3.6``)
* Django (``1.7``, ``1.8``, ``1.9``, ``1.10``, ``1.11``, ``2.0``)
* Django 2.0 is supported with ``Python3.5`` and ``Python3.6``
* Django 1.7 is not for ``Python3.5``

Features
--------
* Multiple model
* Unlimited states
* Multiple destination
* Multiple end-point
* Circular state machines
* Transition authorization
* Skipping or disabling specific step
* Custom transition hooks


Example Scenarios
-----------------
Something Like JIRA
^^^^^^^^^^^^^^^^^^^
Re-Open case
""""""""""""
|Re Open Case|

Closed without Re-Open case
"""""""""""""""""""""""""""
|Closed Without Re Open Case|

Closed with Re-Open case
""""""""""""""""""""""""
|Closed With Re Open Case|


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

-  In your model class which will be processing in workflow;

.. code:: python

    from django.db import models
    from river.models.fields.state import StateField

    class MyModel(models.Model):
        my_state_field = StateField()

.. note::
Once project is configured to work with ``django-river``, do not forget to make your migrations for your model have ``StateField``. Sometimes changes in ``django-river`` models happen. New versions of it might require migrating.

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
There must be only one initial state candidate for your workflow scenarios. Because ``django-river`` is going to try to detect it and initialize your objects workflow path. If there are more than one initial state, ``django-river`` will raise ``RiverException(error_code=3)`` which is ``MULTIPLE_INITIAL_STATE`` error.


Whenever an object of MyModel is inserted in your system, all its
workflow initialization is done by ``django-river``.

Usage for Developer
-------------------

Signals:
^^^^^^^^

``pre_transition``: fired before any transition occurrence.

+-------------------+---------------------------------------+
| Args              | Description                           |
+===================+=======================================+
| workflow_object   | Your object on transition.            |
+-------------------+---------------------------------------+
| source_state      | Transition source state object.       |
+-------------------+---------------------------------------+
| destination_state | Transition destination state object.  |
+-------------------+---------------------------------------+
| proceeding        | Proceeding object.                    |
+-------------------+---------------------------------------+

``post_transition``: fired after any transition occurrence.

+-------------------+---------------------------------------+
| Args              | Description                           |
+===================+=======================================+
| workflow_object   | Your object on transition.            |
+-------------------+---------------------------------------+
| source_state      | Transition source state object.       |
+-------------------+---------------------------------------+
| destination_state | Transition destination state object.  |
+-------------------+---------------------------------------+
| proceeding        | Proceeding object.                    |
+-------------------+---------------------------------------+

``pre_proceed``: fired before any is proceeded. Transition
does not have to occur.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object proceeded.                |
+-----------------+---------------------------------------+
| proceeding      | Proceeding object.                    |
+-----------------+---------------------------------------+

``post_proceed``: fired before any is proceeded occurred.
Transition does not have to occur.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object proceeded.                |
+-----------------+---------------------------------------+
| proceeding      | Proceeding object.                    |
+-----------------+---------------------------------------+


``pre_final``: fired before any workflow is completed.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object on final.                 |
+-----------------+---------------------------------------+

``post_final``: fired after any workflow is completed.

+-----------------+---------------------------------------+
| Args            | Description                           |
+=================+=======================================+
| workflow_object | Your object on final.                 |
+-----------------+---------------------------------------+

Handlers:
---------

Handlers are different from ``django-river`` signals. These are for
specific object, specific source_state, specific destination_state
etc. It is fired when the condition is matched.

PreCompletedHandler:
^^^^^^^^^^^^^^^^^^^^


Before an object is on final state, if the condition is match; means
object is suitable, it is fired;

.. code:: python

    from river.handlers.completed import PreCompletedHandler

    def handler(my_object,*args,**kwargs):
        do_something_with(object)

    PreCompletedHandler.register(handler,my_object)

``register`` method parameter

+-----------------+---------------------------------------+----------+
| Args            | Description                           |          |
+=================+=======================================+==========+
| workflow_object | Your object proceeded                 | Required |
+-----------------+---------------------------------------+----------+

PostCompletedHandler:
^^^^^^^^^^^^^^^^^^^^^

After an object is on final state, if the condition is match; means
object is suitable, it is fired;

.. code:: python

    from river.handlers.completed import PostCompletedHandler

    def handler(my_object,*args,**kwargs):
        do_something_with(object)

    PostCompletedHandler.register(handler,my_object)

``register`` method parameter

+-----------------+---------------------------------------+----------+
| Args            | Description                           |          |
+=================+=======================================+==========+
| workflow_object | Your object proceeded                 | Required |
+-----------------+---------------------------------------+----------+

PreTransitionHandler:
^^^^^^^^^^^^^^^^^^^^^

Before any transition occurred, if the condition is match; means object,
source_state,destination state are suitable, it is fired;

.. code:: python

    from river.handlers.transition import PreTransitionHandler

    def handler(my_object,*args,**kwargs):
        do_something_with(object)

    PreTransitionHandler.register(handler,my_object)

``register`` method parameter

+-------------------+---------------------------------------+----------+
| Args              | Description                           |          |
+===================+=======================================+==========+
| workflow_object   | Your object proceeded                 | Required |
+-------------------+---------------------------------------+----------+
| source_state      | Source state of the transition        | Optional |
+-------------------+---------------------------------------+----------+
| destination_state | Destination state of the transition   | Optional |
+-------------------+---------------------------------------+----------+

PostTransitionHandler:
^^^^^^^^^^^^^^^^^^^^^^

After any transition occurred, if the condition is match; means object,
source_state,destination state are suitable, it is fired;

.. code:: python

    from river.handlers.transition import PostTransitionHandler

    def handler(my_object,*args,**kwargs):
        do_something_with(object)

    PostTransitionHandler.register(handler,my_object)

``register`` method parameter

+-------------------+---------------------------------------+----------+
| Args              | Description                           |          |
+===================+=======================================+==========+
| workflow_object   | Your object   proceeded               | Required |
+-------------------+---------------------------------------+----------+
| source_state      | Source state of the transition        | Optional |
+-------------------+---------------------------------------+----------+
| destination_state | Destination state of the transition   | Optional |
+-------------------+---------------------------------------+----------+

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
^^^^^^^

Indicates states in your state machine.

Transitions:
^^^^^^^^^^^^

These are transition between your states. **There must be only one
initial state** which is in a transition as destination state but no
source state to make ``django-river`` find it on object creation.

Proceeding Meta:
^^^^^^^^^^^^^^^^

These are proceeding meta of transitions that describes which user
permission or user group will be allowed to proceed the transition.
These are kind of template for proceedings will be created for each
object. Putting transitions in order can also be done here. This means,
If you want to put proceeding in order for a transition, you can define it.
Assume **s1** and **s2** are our states and there is a transition
defined between them and we have two proceeding meta on this
transition. They shall be for\ **permission1** and **permission2**. If
you want object available for proceeding; first **permission1** and after it is
proceeded by permission1, then it is on approval the second permission
which is **permission2**, you can do it with ``djang-river`` by defining
order in this model.

Proceeding:
^^^^^^^^^^^

There are state machines paths which is needed to be proceeded for every
particular object. Proceedings are generated on your model object
creation by using ``proceeding meta``. This is whole path for the
created object. Do not add or edit this model data unless you don't need
specific objects editing like skipping, overriding permissions and
groups.

Workflow Manager :
------------------
``django-river`` contains a model manager provides some methods about workflow;

.. code-block:: python
    
    from django.db import models
    from river.models.fields.state import StateField
    from river.models.managers.workflow_object import WorkflowObjectManager
    
    class MyModel(models.Model):
        my_state_field = StateField()

        objects = WorkflowObjectManager()


    >>> MyModel.objects.get_objects_waiting_for_approval(current_user)
    # Will give you your model instance objects which is waiting for approval by current user by considering his/her authorization rules.

    >>> MyModel.objects.get_object_count_waiting_for_approval(current_user)
    # Will give you count of your model instance objects which is waiting for approval by current user by considering his/her authorization rules. This can be used to show a badge contains a count on main screen for each user whether there are some objects waiting for approval.



Timeline
--------

|Timeline|


Change Logs
===========

0.10.0(Development)
------------------

* # 39_ - **Improvement** -  Django has dropped support for pypy-3. So, It should be dropped from django itself too.
* **Remove** -  ``pypy`` support has been dropped
* **Remove** -  ``Python3.3`` support has been dropped
* **Improvement** - ``Django2.0`` support with ``Python3.5`` and ``Python3.6`` is provided

.. _39: https://github.com/javrasya/django-river/issues/39

0.9.0(Stable)
-------------

* # 30_ - **Bug** -  Missing migration file which is ``0007`` because of ``Python2.7`` can not detect it.
* # 31_ - **Improvement** - unicode issue for Python3.
* # 33_ - **Bug** - Automatically injecting workflow manager was causing the models not have default ``objects`` one. So, automatic injection support has been dropped. If anyone want to use it, it can be used explicitly.
* # 35_ - **Bug** - This is huge change in django-river. Multiple state field each model support is dropped completely and so many APIs have been changed. Check documentations and apply changes.

.. _30: https://github.com/javrasya/django-river/pull/30
.. _31: https://github.com/javrasya/django-river/pull/30
.. _33: https://github.com/javrasya/django-river/pull/33
.. _35: https://github.com/javrasya/django-river/pull/35

0.8.2
-----

* **Bug** - Features providing multiple state field in a model was causing a problem. When there are multiple state field, injected attributes in model class are owerriten. This feature is also unpractical. So, it is dropped to fix the bug.
* **Improvement** - Initial video tutorial which is Simple jira example is added into the documentations. Also repository link of fakejira project which is created in the video tutorial is added into the docs.
* **Improvement** - No proceeding meta parent input is required by user. It is set automatically by django-river now. The field is removed from ProceedingMeta admin interface too.


0.8.1
-----

* **Bug** - ProceedingMeta form was causing a problem on migrations. Accessing content type before migrations was the problem. This is fixed by defining choices in init function instead of in field

0.8.0
-----

* **Deprecation** - ProceedingTrack is removed. ProceedingTracks were being used to keep any transaction track to handle even circular one. This was a workaround. So, it can be handled with Proceeding now by cloning them if there is circle. ProceedingTracks was just causing confusion. To fix this, ProceedingTrack model and its functions are removed from django-river.
* **Improvement** - Circular scenario test is added.
* **Improvement** - Admins of the workflow components such as State, Transition and ProceedingMeta are registered automatically now. Issue #14 is fixed.

0.7.0
-----

* **Improvement** - Python version 3.5 support is added. (not for Django1.7)
* **Improvement** - Django version 1.9 support is added. (not for Python3.3 and PyPy3)

0.6.2
-----

* **Bug** - Migration ``0002`` and ``0003`` were not working properly for postgresql (maybe oracle). For these databases, data can not be fixed. Because, django migrates each in a transactional block and schema migration and data migration can not be done in a transactional block. To fix this, data fixing and schema fixing are separated.
* **Improvement** - Timeline section is added into documentation.
* **Improvement** - State slug field is set as slug version of its label if it is not given on saving.

0.6.1
-----

* **Bug** - After ``content_type`` and ``field`` are moved into ``ProceedingMeta`` model from ``Transition`` model in version ``0.6.0``, finding initial and final states was failing. This is fixed.
* **Bug** - ``0002`` migrations was trying to set default slug field of State model. There was a unique problem. It is fixed. ``0002`` can be migrated now.
* **Improvement** - The way of finding initial and final states is changed. ProceedingMeta now has parent-child tree structure to present state machine. This tree structure is used to define the way. This requires to migrate ``0003``. This migration will build the tree of your existed ProceedingMeta data.



0.6.0
-----

* **Improvement** - ``content_type`` and ``field`` are moved into ``ProceedingMeta`` model from ``Transition`` model. This requires to migrate ``0002``. This migrations will move value of the fields from ``Transition`` to ``ProceedingMeta``.
* **Improvement** - Slug field is added in ``State``. It is unique field to describe state. This requires to migrate ``0002``. This migration will set the field as slug version of ``label`` field value. (Re Opened -> re-opened)
* **Improvement** - ``State`` model now has ``natural_key`` as ``slug`` field.
* **Improvement** - ``Transition`` model now has ``natural_key`` as (``source_state_slug`` , ``destination_state_slug``) fields
* **Improvement** - ``ProceedingMeta`` model now has ``natural_key`` as (``content_type``, ``field``, ``transition``, ``order``) fields
* **Improvement** - Changelog is added into documentation.

0.5.3
-----

* **Bug** - Authorization was not working properly when the user has irrelevant permissions and groups. This is fixed.
* **Improvement** - User permissions are now retrieved from registered authentication backends instead of ``user.user_permissions``
  

0.5.2
-----

* **Improvement** - Removed unnecessary models.
* **Improvement** - Migrations are added
* **Bug** - ``content_type__0002`` migrations cause failing for ``django1.7``. Dependency is removed
* **Bug** - ``DatabaseHandlerBacked`` was trying to access database on django setup. This cause ``no table in db`` error for some django commands. This was happening; because there is no db created before some commands are executed; like ``makemigrations``, ``migrate``.


0.5.1
-----

* **Improvement** - Example scenario diagrams are added into documentation.
* **Bug** - Migrations was failing because of injected ``ProceedingTrack`` relation. Relation is not injected anymore. But property ``proceeding_track`` remains. It still returns current one.
  


.. image:: https://d2weczhvl823v0.cloudfront.net/javrasya/django-river/trend.png
    :alt: Bitdeli badge
   :target: https://bitdeli.com/free

