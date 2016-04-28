.. _change_logs:

Change Logs
===========

0.8.0 (Dev)
-----------

* **Deprecation** - ProceedingTrack is removed. ProceedingTracks were being used to keep any transaction track to handle even circular one. This was a workaround. So, it can be handled with Proceeding now by cloning them if there is circle. ProceedingTracks was just causing confusion. To fix this, ProceedingTrack model and its functions are removed from django-river.
* **Improvement** - Circular scenario test is added.

0.7.0 (Stable)
--------------

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