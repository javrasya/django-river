.. _instance_api_guide:

Instance API
============

This page will be covering the instance level API. It is all the function that you can access through your model object 
like in the example below;

    .. code-block:: python

        my_model=MyModel.objects.get(....)
        
        my_model.river.my_state_field.<function>(*args)


approve
-------

This is the function that helps you to approve next approval of the object easily. ``django-river`` will handle all
the availibility and the authorization issues. 

>>> my_model.river.my_state_field.approve(as_user=team_leader)
>>> my_model.river.my_state_field.approve(as_user=team_leader, next_state=State.objects.get(name='re_opened_state'))

+------------+-------+---------+------------+-------------+-----------------------------------------+
|            | Type  | Default |  Optional  |   Format    |               Description               |
+============+=======+=========+============+=============+=========================================+
| as_user    | input | NaN     | False      | Django User | | A user to make the transaction.       |
|            |       |         |            |             | | ``django-river`` will check           |
|            |       |         |            |             | | if this user is authorized to         |
|            |       |         |            |             | | make next action by looking at        |
|            |       |         |            |             | | this user's permissions and           |
|            |       |         |            |             | | user groups.                          |
+------------+-------+---------+------------+-------------+-----------------------------------------+
| next_state | input | NaN     | True/False | State       | | This parameter is redundant           |
|            |       |         |            |             | | as long as there is only one          |
|            |       |         |            |             | | next state from the current           |
|            |       |         |            |             | | state. But if there is multiple       |
|            |       |         |            |             | | possible next state in place,         |
|            |       |         |            |             | | ``django-river`` is naturally         |
|            |       |         |            |             | | is unable know which one is           |
|            |       |         |            |             | | actually supposed to be picked.       |
|            |       |         |            |             | | If the given next state is not        |
|            |       |         |            |             | | a valid next state a `RiverException` |
|            |       |         |            |             | | will be thrown.                       |
+------------+-------+---------+------------+-------------+-----------------------------------------+
| god_mod    | input | False   | True       | Boolean     | | Authorization will be skipped if      |
|            |       |         |            |             | | this is `True`                        |
+------------+-------+---------+------------+-------------+-----------------------------------------+

get_available_approvals
-----------------------

This is the function that helps you to fetch all available approvals waiting for a spesific user according to given source and
destination states. If the source state is not provided, ``django-river`` will pick the current objects source state.

>>> transition_approvals = my_model.river.my_state_field.get_available_approvals(as_user=manager)
>>> transition_approvals = my_model.river.my_state_field.get_available_approvals(as_user=manager, source_state=State.objects.get(name='in_progress'))
>>> transition_approvals = my_model.river.my_state_field.get_available_approvals(
        as_user=manager, 
        source_state=State.objects.get(name='in_progress'),
        destination_state=State.objects.get(name='resolved'),
    )

+-------------------+--------+----------------+----------+--------------------------+------------------------------------------+
|                   |  Type  |    Default     | Optional |          Format          |               Description                |
+===================+========+================+==========+==========================+==========================================+
| as_user           | input  | NaN            | False    | Django User              | | A user to find all the approvals       |
|                   |        |                |          |                          | | by user's permissions and groups       |
+-------------------+--------+----------------+----------+--------------------------+------------------------------------------+
| source_state      | input  | | Current      | True     | State                    | | A base state to find all available     |
|                   |        | | Object's     |          |                          | | approvals comes after. Default is      |
|                   |        | | Source State |          |                          | | current object's source state          |
+-------------------+--------+----------------+----------+--------------------------+------------------------------------------+
| destination_state | input  | NaN            | True     | State                    | | A spesific destination state to        |
|                   |        |                |          |                          | | fetch all available state. If it       |
|                   |        |                |          |                          | | is not provided, the approvals         |
|                   |        |                |          |                          | | will be found for all available        |
|                   |        |                |          |                          | | destination states                     |
+-------------------+--------+----------------+----------+--------------------------+------------------------------------------+
| god_mod           | input  | False          | True     | Boolean                  | | Authorization will be skipped if       |
|                   |        |                |          |                          | | this is `True`                         |
+-------------------+--------+----------------+----------+--------------------------+------------------------------------------+
|                   | Output |                |          | List<TransitionApproval> | | List of available transition approvals |
+-------------------+--------+----------------+----------+--------------------------+------------------------------------------+

recent_approval
-------------

This is a property that the transition approval which has recently been approved for the model object.

>>> transition_approval = my_model.river.my_state_field.last_approval

+--------+--------------------+-------------------------------------+
|  Type  |       Format       |             Description             |
+========+====================+=====================================+
| Output | TransitionApproval | | Last approved transition approval |
|        |                    | | for the model object              |
+--------+--------------------+-------------------------------------+

next_approvals
--------------

This is a property that the list of transition approvals as a next step.

>>> transition_approvals = my_model.river.my_state_field.next_approvals

+--------+--------------------------+--------------------------------------+
|  Type  |          Format          |             Description              |
+========+==========================+======================================+
| Output | List<TransitionApproval> | | List of transition approvals comes |
|        |                          | | after last approved transition     |
|        |                          | | approval                           |
+--------+--------------------------+--------------------------------------+


on_initial_state
--------------

This is a property that indicates if object is on initial state.

>>> True == my_model.river.my_state_field.on_initial_state

+--------+---------+------------------------------------+
|  Type  | Format  |            Description             |
+========+=========+====================================+
| Output | Boolean | True if object is on initial state |
+--------+---------+------------------------------------+

on_final_state
--------------

This is a property that indicates if object is on final state.

>>> True == my_model.river.my_state_field.on_final_state

+--------+---------+--------------------------------------+
|  Type  | Format  |             Description              |
+========+=========+======================================+
| Output | Boolean | | True if object is on final state   |
|        |         | | which also means that the workflow |
|        |         | | is complete                        |
+--------+---------+--------------------------------------+

.. _instance_api_hooking_pre_transition:

hook_pre_transition
--------------------

This is a function that helps you to hook pre-transtion. This is gonna be executed only for the model object which it has been registered with.
For more detail please look at :ref:`transition_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name, transition_approval=None, source_state=None, destination_state=None):
            pass
        
    >>> my_model.river.my_state_field.hook_pre_transition(my_callback)
    >>> my_model.river.my_state_field.hook_pre_transition(my_callback, source_state=in_progress_state, destination_state=resolved_state)

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

.. _instance_api_hooking_post_transition:

hook_post_transition
--------------------

This is a function that helps you to hook post-transtion. This is gonna be executed only for the model object which it has been registered with.
For more detail please look at :ref:`transition_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name, transition_approval=None):
            pass
        
    >>> my_model.river.my_state_field.hook_post_transition(my_callback)
    >>> my_model.river.my_state_field.hook_post_transition(my_callback, source_state=in_progress_state, destination_state=resolved_state)

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

.. _instance_api_hooking_pre_completion:

hook_pre_complete
--------------------

This is a function that helps you to hook pre-complete. This is gonna be executed only for the model object which it has been registered with.
For more detail please look at :ref:`on_complete_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name):
            pass
        
    >>> my_model.river.my_state_field.hook_pre_complete(my_callback)

+----------+-------+---------+----------+----------+---------------------------------------------+
|          | Type  | Default | Optional |  Format  |                 Description                 |
+==========+=======+=========+==========+==========+=============================================+
| callback | input | NaN     | False    | Callable | | A callback function for ``django-river``  |
|          |       |         |          |          | | to call when the given transition happens |
+----------+-------+---------+----------+----------+---------------------------------------------+

.. _instance_api_hooking_post_completion:

hook_post_complete
--------------------

This is a function that helps you to hook post-complete. This is gonna be executed only for the model object which it has been registered with.
For more detail please look at :ref:`on_complete_callback_function`.

    .. code-block:: python

        def my_callback(workflow_obj, field_name):
            pass
        
    >>> my_model.river.my_state_field.hook_post_complete(my_callback)

+----------+-------+---------+----------+----------+---------------------------------------------+
|          | Type  | Default | Optional |  Format  |                 Description                 |
+==========+=======+=========+==========+==========+=============================================+
| callback | input | NaN     | False    | Callable | | A callback function for ``django-river``  |
|          |       |         |          |          | | to call when the given transition happens |
+----------+-------+---------+----------+----------+---------------------------------------------+

.. toctree::
    :maxdepth: 2