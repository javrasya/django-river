.. _change_logs:

Change Logs
===========

3.2.2 (Stable):
---------------
    * **Bug**         -  # 162_: Fix a bug that is causing some possible future transitions to turn to CANCELLED for some workflows.

.. _162: https://github.com/javrasya/django-river/issues/159

3.2.1:
------
    * **Bug**         -  # 159_: A bug that is with having multiple cyclic dependencies in a workflow that happens when one of tem goes through has been fixed.
    * **Drop**        -        : Drop Python3.4 support since it is having incompatibilities with the module ``six``


.. _159: https://github.com/javrasya/django-river/issues/159

3.2.0:
------
    * **Improvement** -  # 140_ 141_: Support Microsoft SQL Server 17 and 19


.. _140: https://github.com/javrasya/django-river/issues/140
.. _141: https://github.com/javrasya/django-river/issues/141

3.1.4:
------
    * **Bug**         -  # 137_: Fix a bug with jumping to a state


.. _137: https://github.com/javrasya/django-river/issues/137

3.1.3:
------
    * **Improvement** -  # 135_: Support Django 3.0


.. _135: https://github.com/javrasya/django-river/issues/135


3.1.2:
------
    * **Improvement** -  # 133_: Support MySQL 8.0


.. _133: https://github.com/javrasya/django-river/issues/133

3.1.1
-----
    * **Bug**         -  # 128_: Available approvals are not found properly when primary key is string
    * **Bug**         -  # 129_: Models with string typed primary keys violates integer field in the hooks


.. _128: https://github.com/javrasya/django-river/issues/128
.. _129: https://github.com/javrasya/django-river/issues/129

3.1.0
-----
    * **Imrovement**  -  # 123_: Jump to a specific future state of a workflow object
    * **Bug**         -  # 124_: Include some BDD tests for the users to understand the usages easier.


.. _123: https://github.com/javrasya/django-river/issues/123
.. _124: https://github.com/javrasya/django-river/issues/124

3.0.0
-----
    * **Bug**         -  # 106_: It crashes when saving a workflow object when there is no workflow definition for a state field
    * **Bug**         -  # 107_: next_approvals api of the instance is broken
    * **Bug**         -  # 112_: Next approval after it cycles doesn't break the workflow anymore. Multiple cycles are working just fine.
    * **Improvement** -  # 108_: Status column of transition approvals are now kept as string in the DB instead of number to maintain readability and avoid mistakenly changed ordinals.
    * **Improvement** -  # 109_: Cancel all other peer approvals that are with different branching state.
    * **Improvement** -  # 110_: Introduce an iteration to keep track of the order of the transitions even the cycling ones. This comes with a migration that will assess the iteration of all of your existing approvals so far. According to the tests, 250 workflow objects that have 5 approvals each will take ~1 minutes with the slowest django `v1.11`.
    * **Improvement** -  # 111_: Cancel all approvals that are not part of the possible future instead of only impossible the peers when something approved and re-create the whole rest of the pipeline when it cycles
    * **Improvement** -  # 105_: More dynamic and better way for hooks.On the fly function and hook creations, update or delete are also supported now. It also comes with useful admin interfaces for hooks and functions. This is a huge improvement for callback lovers :-)
    * **Improvement** -  # 113_: Support defining an approval hook with a specific approval.
    * **Improvement** -  # 114_: Support defining a transition hook with a specific iteration.
    * **Drop** -         # 115_: Drop skipping and disabling approvals to cut the unnecessary complexity.
    * **Improvement** -  # 116_: Allow creating transitions without any approvals. A new TransitionMeta and Transition models are introduced to keep transition information even though there is no transition approval yet.


.. _105: https://github.com/javrasya/django-river/issues/105
.. _106: https://github.com/javrasya/django-river/issues/106
.. _107: https://github.com/javrasya/django-river/issues/107
.. _108: https://github.com/javrasya/django-river/issues/108
.. _109: https://github.com/javrasya/django-river/issues/109
.. _110: https://github.com/javrasya/django-river/issues/110
.. _111: https://github.com/javrasya/django-river/issues/110
.. _112: https://github.com/javrasya/django-river/issues/112
.. _113: https://github.com/javrasya/django-river/issues/113
.. _114: https://github.com/javrasya/django-river/issues/114
.. _115: https://github.com/javrasya/django-river/issues/115
.. _116: https://github.com/javrasya/django-river/issues/116

2.0.0
-----
    * **Improvement** -  [ # 90_,# 36_ ]: Finding available approvals has been speeded up ~x400 times at scale
    * **Improvement** -  # 92_ : It is mandatory to provide initial state by the system user to avoid confusion and possible mistakes
    * **Improvement** -  # 93_ : Tests are revisited, separated, simplified and easy to maintain right now
    * **Improvement** -  # 94_ : Support class level hooking. Meaning that, a hook can be registered for all the objects through the class api
    * **Bug** -  # 91_ : Callbacks get removed when the related workflow object is deleted
    * **Improvement** -  Whole ``django-river`` source code is revisited and simplified
    * **Improvement** -  Support ``Django v2.2``
    * **Deprecation** -  ``Django v1.7``, ``v1.8``, ``v1.9`` and ``v1.10`` supports have been dropped

.. _36: https://github.com/javrasya/django-river/issues/36
.. _90: https://github.com/javrasya/django-river/issues/90
.. _91: https://github.com/javrasya/django-river/issues/91
.. _92: https://github.com/javrasya/django-river/issues/92
.. _93: https://github.com/javrasya/django-river/issues/93
.. _94: https://github.com/javrasya/django-river/issues/94

1.0.2
-----
    * **Bug** - # 77_ : Migrations for the models that have state field is no longer kept getting recreated.
    * **Bug** - It is crashing when there is no workflow in the workspace.

.. _77: https://github.com/javrasya/django-river/issues/77


1.0.1
-----
    * **Bug** - # 74_ : Fields that have no transition approval meta are now logged correctly.
    * **Bug** - ``django`` version is now fixed to 2.1 for coverage in the build to make the build pass

.. _74: https://github.com/javrasya/django-river/issues/74

1.0.0
-----
``django-river`` is finally having it's first major version bump. In this version, all code and the APIs are revisited
and are much easier to understand how it works and much easier to use it now. In some places even more performant. 
There are also more documentation with this version. Stay tuned :-)

    * **Improvement** - Support ``Django2.1``
    * **Improvement** - Support multiple state fields in a model
    * **Improvement** - Make the API very easy and useful by accessing everything via model objects and model classes
    * **Improvement** - Simplify the concepts
    * **Improvement** - Migrate ProceedingMeta and Transition into TransitionApprovalMeta for simplification
    * **Improvement** - Rename Proceeding as TransitionApproval
    * **Improvement** - Document transition and on-complete hooks
    * **Improvement** - Document transition and on-complete hooks
    * **Improvement** - Imrove documents in general
    * **Improvement** - Minor improvements on admin pages
    * **Improvement** - Some performance improvements

0.10.0
------

    * # 39_ - **Improvement** -  Django has dropped support for pypy-3. So, It should be dropped from django itself too.
    * **Remove** -  ``pypy`` support has been dropped
    * **Remove** -  ``Python3.3`` support has been dropped
    * **Improvement** - ``Django2.0`` support with ``Python3.5`` and ``Python3.6`` is provided

.. _39: https://github.com/javrasya/django-river/issues/39

0.9.0
-----

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

    * **Bug** - Migration ``0002`` and ``0003`` were not working properly for postgresql (maybe oracle). For these databases, data can not be fixed. Because, django migrates each in a transactional block and schema migration and data migration can not be done in a transactional block. To fix this, data fixing and schema fixing are seperated.
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
    * **Improvement** - User permissions are now retreived from registered authentication backends instead of ``user.user_permissions``
  

0.5.2
-----

    * **Improvement** - Removed unnecessary models.
    * **Improvement** - Migrations are added
    * **Bug** - ``content_type__0002`` migrations cause failing for ``django1.7``. Dependency is removed
    * **Bug** - ``DatabaseHandlerBacked`` was trying to access database on django setup. This cause ``no table in db`` error for some django commands. This was happening; because there is no db created before some commands are executed; like ``makemigrations``, ``migrate``.


0.5.1
-----

    * **Improvement** - Example scenario diagrams are added into documentation.
    * **Bug** - Migrations was failing because of injected ``ProceedingTrack`` relation. Relation is not injected anymore. But property ``proceeing_track`` remains. It still returns current one.
