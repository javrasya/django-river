.. _developer_guide:

Advance Guide
=============

StateField
----------
``StateField`` is a model field defined in ``django-river``, which prepares everything for you. Whenever you put this field into a model object, the model converts into a workflow model. The model have some workflow specialized properties, methods and relations.

Arguments
^^^^^^^^^

+-------------+---------------------------------------------------------------------------------------------------------------------------+
| Arguments   | Description                                                                                                               |
+=============+===========================================================================================================================+
| state_model | You can change your state model. State model in ``django-river`` is used as default. It is recomended to use default one. |
+-------------+---------------------------------------------------------------------------------------------------------------------------+



The Model Injections
^^^^^^^^^^^^^^^^^^^^
``django-river`` injects some properties, relations and methods into your model class. This means, ther is gonna be special workflow properties, relations and methods in your model objects. Assume that your model class is ``Ticket``; When you have a ticket object, you can access the injections like ``ticket.any_injection_below`` or ``ticket.any_injection_below.all()`` or ``ticket.any_injection_below()``.


Properties:
"""""""""""

+-----------------------------+-------------------------+------------------------------------------------------------------+
| Name                        | Return Type             | Description                                                      |
+=============================+=========================+==================================================================+
| ``on_initial_state:``       | ``boolean``             | Defines your model object is on initial states or not.           |
+-----------------------------+-------------------------+------------------------------------------------------------------+
| ``on_final_state:``         | ``boolean``             | Defines your model object is on final states or not.             |
+-----------------------------+-------------------------+------------------------------------------------------------------+
| ``on_initial_proceedings:`` | ``Proceeding Queryset`` | Returns initial proceeding objects.                              |
+-----------------------------+-------------------------+------------------------------------------------------------------+
| ``on_final_proceedings:``   | ``Proceeding Queryset`` | Returns final proceeding objects.                                |
+-----------------------------+-------------------------+------------------------------------------------------------------+
| ``next_proceedings:``       | ``Proceeding Queryset`` | Returns next proceedings objects according to the current state. |
+-----------------------------+-------------------------+------------------------------------------------------------------+



Methods:
""""""""

+--------------+-------------+-------------------------------------------------------------------+--------------------------------------------------------+
| Name         | Return Type | Parameters                                                        | Description                                            |
+==============+=============+===================================================================+========================================================+
| ``proceed:`` | ``boolean`` | ``user``(must): User is gonna proceed, ``next_state``(not always) | Defines your model object is on initial states or not. |
+--------------+-------------+-------------------------------------------------------------------+--------------------------------------------------------+



Relations:
""""""""""

+-----------------------+---------------------+---------------------------+
| Name                  | Type                | Description               |
+=======================+=====================+===========================+
| ``proceedings:``      | ``GenericRelation`` | To Proceeding model.      |
+-----------------------+---------------------+---------------------------+
| ``proceeding_tract:`` | ``ForeignKey``      | To Proceeding Track model |
+-----------------------+---------------------+---------------------------+


Signals
-------

``pre_transition``: it is fired before any transition occured.

+-------------------+---------------------------------------+
| **Args**          | **Description**                       |
+===================+=======================================+
| workflow_object   | Your object on transition             |
+-------------------+---------------------------------------+
| field             | Field which you registered object for |
+-------------------+---------------------------------------+
| source_state      | Transition source state object        |
+-------------------+---------------------------------------+
| destination_state | Transition destination state object   |
+-------------------+---------------------------------------+
| proceeder         | Proceeding object                     |
+-------------------+---------------------------------------+

``post_transition``: it is fired before any transition occured.

+-------------------+---------------------------------------+
| **Args**          | **Description**                       |
+===================+=======================================+
| workflow_object   | Your object on transition             |
+-------------------+---------------------------------------+
| field             | Field which you registered object for |
+-------------------+---------------------------------------+
| source_state      | Transition source state object        |
+-------------------+---------------------------------------+
| destination_state | Transition destination state object   |
+-------------------+---------------------------------------+
| proceeder        | Proceeding object                    |
+-------------------+---------------------------------------+


``pre_proceeded``: it is fired before any is proceeded. Transition does not have to be occured.

+-----------------+---------------------------------------+
| **Args**        | **Description**                       |
+=================+=======================================+
| workflow_object | Your object proceeded                 |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+
| proceeder       | Proceeding object                     |
+-----------------+---------------------------------------+
| track           | Proceeding track object               |
+-----------------+---------------------------------------+

``post_proceeded``: it is fired before any is proceeded. Transition does not have to be occured.

+-----------------+---------------------------------------+
| **Args**        | **Description**                       |
+=================+=======================================+
| workflow_object | Your object proceeded                 |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+
| proceeder       | Proceeding object                     |
+-----------------+---------------------------------------+
| track           | Proceeding track object               |
+-----------------+---------------------------------------+

``pre_final``: it is fired before any workflow is completed.

+-----------------+---------------------------------------+
| **Args**        | **Description**                       |
+=================+=======================================+
| workflow_object | Your object on final                  |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+

``post_final``: it is fired before any workflow is completed.

+-----------------+---------------------------------------+
| **Args**        | **Description**                       |
+=================+=======================================+
| workflow_object | Your object on final                  |
+-----------------+---------------------------------------+
| field           | Field which you registered object for |
+-----------------+---------------------------------------+





Handlers
--------
Handlers are different from `django-river`. These are for spesific object, spesific source_state, spesific destination_state etc. It is fired when the condition is matched.

PreCompletedHandler
^^^^^^^^^^^^^^^^^^^^
Before an object is on final state, if the condition is match; means object is suitable, it is fired;

.. code-block:: python

    from river.handlers.completed import PreCompletedHandler

    def handler(my_object,field,*args,**kwargs):
	    do_something_with(object,field)

    PreCompletedHandler.register(handler,my_object,'my_state_field')
	
	


``register`` method parameter**

+-----------------+---------------------------------------+----------+
| **Args**        | **Description**                       |          |
+=================+=======================================+==========+
| workflow_object | Your object                           | Required |
+-----------------+---------------------------------------+----------+
| field           | Field which you registered object for | Required |
+-----------------+---------------------------------------+----------+

PostCompletedHandler
^^^^^^^^^^^^^^^^^^^^^
After an object is on final state, if the condition is match; means object is suitable, it is fired;


.. code-block:: python

    from river.handlers.completed import PostCompletedHandler

    def handler(my_object,field,*args,**kwargs):
        do_something_with(object,field)
    
    PostCompletedHandler.register(handler,my_object,'my_state_field')


**`register` method parameter**

+-----------------+---------------------------------------+----------+
| **Args**        | **Description**                       |          |
+=================+=======================================+==========+
| workflow_object | Your object                           | Required |
+-----------------+---------------------------------------+----------+
| field           | Field which you registered object for | Required |
+-----------------+---------------------------------------+----------+

PreTransitionHandler
^^^^^^^^^^^^^^^^^^^^^
Before any transition occurred, if the condition is match; means object, source_state,destination state are suitable, it is fired;

.. code-block:: python

    from river.handlers.transition import PreTransitionHandler

    def handler(my_object,field,*args,**kwargs):
        do_something_with(object,field)

    PreTransitionHandler.register(handler,my_object,'my_state_field')


**`register` method parameter**

+------------------+---------------------------------------+----------+
| **Args**         | **Description**                       |          |
+==================+=======================================+==========+
| workflow_object  | Your object  proceeded                | Required |
+------------------+---------------------------------------+----------+
| field            | Field which you registered object for | Required |
+------------------+---------------------------------------+----------+
| source_state     | Source state of the tranition         | Optional |
+------------------+---------------------------------------+----------+
| desination_satte | Destinatio state of the tranition     | Optional |
+------------------+---------------------------------------+----------+

PostTransitionHandler
^^^^^^^^^^^^^^^^^^^^^^
After any transition occurred, if the condition is match; means object, source_state,destination state are suitable, it is fired;

.. code-block:: python

    from river.handlers.transition import PostTransitionHandler
    
    def handler(my_object,field,*args,**kwargs):
        do_something_with(object,field)

    PostTransitionHandler.register(handler,my_object,'my_state_field')


**`register` method parameter**

+------------------+---------------------------------------+----------+
| **Args**         | **Description**                       |          |
+==================+=======================================+==========+
| workflow_object  | Your object proceeded                 | Required |
+------------------+---------------------------------------+----------+
| field            | Field which you registered object for | Required |
+------------------+---------------------------------------+----------+
| source_state     | Source state of the tranition         | Optional |
+------------------+---------------------------------------+----------+
| desination_satte | Destinatio state of the tranition     | Optional |
+------------------+---------------------------------------+----------+


Handler Backends
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
