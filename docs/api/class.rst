.. _class_api_guide:

Class API
=========

This page will be covering the class level API. It is all the function that you can access through your model class 
like in the example below;

>>> MyModel.river.my_state_field.<function>(*args)

get_on_approval_objects
-----------------------

This is the function that helps you to fetch all model objects waitig for a users approval.

>>> my_model_objects == MyModel.river.my_state_field.get_on_approval_objects(as_user=team_leader)
True

+---------+--------+---------+----------+---------------+----------------------------------------+
|         |  Type  | Default | Optional |    Format     |              Description               |
+=========+========+=========+==========+===============+========================================+
| as_user | input  | NaN     | False    | Django User   | | A user to find all the model objects |
|         |        |         |          |               | | waiting for a user's approvals       |
+---------+--------+---------+----------+---------------+----------------------------------------+
|         | Output |         |          | List<MyModel> | | List of available my model objects   |
+---------+--------+---------+----------+---------------+----------------------------------------+


initial_state
-------------
This is a property that is the initial state in the workflow

>>> State.objects.get(label="open") == MyModel.river.my_state_field.initial_state
True


+--------+--------+-----------------------------------+
|  Type  | Format |            Description            |
+========+========+===================================+
| Output | State  | The initial state in the workflow |
+--------+--------+-----------------------------------+

final_states
-------------
This is a property that is the list of final state in the workflow

>>> State.objects.filter(Q(label="closed") | Q(label="cancelled")) == MyModel.river.my_state_field.final_states
True


+--------+-------------+------------------------------------------+
|  Type  |   Format    |               Description                |
+========+=============+==========================================+
| Output | List<State> | List of the final states in the workflow |
+--------+-------------+------------------------------------------+

.. _class_api_hooking_pre_transition:

hook_pre_transition
--------------------

This is a function that helps you to hook pre-transtion. This is gonna be executed for every object.
For more detail please look at :ref:`transition_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name, transition_approval=None, source_state=None, destination_state=None):
            pass

    >>> MyModelClass.river.my_state_field.hook_pre_transition(my_callback)
    >>> MyModelClass.river.my_state_field.hook_pre_transition(my_callback, source_state=in_progress_state, destination_state=resolved_state)

+-------------------+-------+---------+----------+----------+---------------------------------------------+
|                   | Type  | Default | Optional |  Format  |                 Description                 |
+===================+=======+=========+==========+==========+=============================================+
| callback          | input | NaN     | False    | Callable | | A callback function for ``django-river``  |
|                   |       |         |          |          | | to call when the given transition happens |
+-------------------+-------+---------+----------+----------+---------------------------------------------+
| source_state      | input | NaN     | True     | State    | | Spesific source state for the hook        |
+-------------------+-------+---------+----------+----------+---------------------------------------------+
| destination_state | input | NaN     | True     | State    | | Spesific destination state for the hook   |
+-------------------+-------+---------+----------+----------+---------------------------------------------+

.. _class_api_hooking_post_transition:

hook_post_transition
--------------------

This is a function that helps you to hook post-transtion. This is gonna be executed for every object.
For more detail please look at :ref:`transition_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name, transition_approval=None):
            pass

    >>> MyModelClass.river.my_state_field.hook_post_transition(my_callback)
    >>> MyModelClass.river.my_state_field.hook_post_transition(my_callback, source_state=in_progress_state, destination_state=resolved_state)

+-------------------+-------+---------+----------+----------+---------------------------------------------+
|                   | Type  | Default | Optional |  Format  |                 Description                 |
+===================+=======+=========+==========+==========+=============================================+
| callback          | input | NaN     | False    | Callable | | A callback function for ``django-river``  |
|                   |       |         |          |          | | to call when the given transition happens |
+-------------------+-------+---------+----------+----------+---------------------------------------------+
| source_state      | input | NaN     | True     | State    | | Spesific source state for the hook        |
+-------------------+-------+---------+----------+----------+---------------------------------------------+
| destination_state | input | NaN     | True     | State    | | Spesific destination state for the hook   |
+-------------------+-------+---------+----------+----------+---------------------------------------------+

.. _class_api_hooking_pre_completion:

hook_pre_complete
--------------------

This is a function that helps you to hook pre-complete. This is gonna be executed for every object.
For more detail please look at :ref:`on_complete_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name):
            pass

    >>> MyModelClass.river.my_state_field.hook_pre_complete(my_callback)

+----------+-------+---------+----------+----------+---------------------------------------------+
|          | Type  | Default | Optional |  Format  |                 Description                 |
+==========+=======+=========+==========+==========+=============================================+
| callback | input | NaN     | False    | Callable | | A callback function for ``django-river``  |
|          |       |         |          |          | | to call when the given transition happens |
+----------+-------+---------+----------+----------+---------------------------------------------+

.. _class_api_hooking_post_completion:

hook_post_complete
--------------------

This is a function that helps you to hook post-complete. This is gonna be executed for every object.
For more detail please look at :ref:`on_complete_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name):
            pass

    >>> MyModelClass.river.my_state_field.hook_post_complete(my_callback)

+----------+-------+---------+----------+----------+---------------------------------------------+
|          | Type  | Default | Optional |  Format  |                 Description                 |
+==========+=======+=========+==========+==========+=============================================+
| callback | input | NaN     | False    | Callable | | A callback function for ``django-river``  |
|          |       |         |          |          | | to call when the given transition happens |
+----------+-------+---------+----------+----------+---------------------------------------------+

.. toctree::
    :maxdepth: 2