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
the availability and the authorization issues.

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

get_available_approvals
-----------------------

This is the function that helps you to fetch all available approvals waiting for a specific user according to given source and
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
| destination_state | input  | NaN            | True     | State                    | | A specific destination state to        |
|                   |        |                |          |                          | | fetch all available state. If it       |
|                   |        |                |          |                          | | is not provided, the approvals         |
|                   |        |                |          |                          | | will be found for all available        |
|                   |        |                |          |                          | | destination states                     |
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

>>> transition_approvals == my_model.river.my_state_field.next_approvals
True

+--------+--------------------------+--------------------------------------+
|  Type  |          Format          |             Description              |
+========+==========================+======================================+
| Output | List<TransitionApproval> | | List of transition approvals comes |
|        |                          | | after last approved transition     |
|        |                          | | approval                           |
+--------+--------------------------+--------------------------------------+


on_initial_state
----------------

This is a property that indicates if object is on initial state.

>>> my_model.river.my_state_field.on_initial_state
True

+--------+---------+------------------------------------+
|  Type  | Format  |            Description             |
+========+=========+====================================+
| Output | Boolean | True if object is on initial state |
+--------+---------+------------------------------------+

on_final_state
--------------

This is a property that indicates if object is on final state.

>>> my_model.river.my_state_field.on_final_state
True

+--------+---------+--------------------------------------+
|  Type  | Format  |             Description              |
+========+=========+======================================+
| Output | Boolean | | True if object is on final state   |
|        |         | | which also means that the workflow |
|        |         | | is complete                        |
+--------+---------+--------------------------------------+

jump_to
-------

This is the function that allows to jump to a specific future state
from the current state of the workflow object. It is good for testing
purposes.

>>> in_progress_state = State.object.get(label="In Progress")
>>> transition_approvals = my_model.river.my_state_field.jump_to(in_progress_state)

+-------------------+--------+--------------------------+------------------------------------------+
|                   |  Type  |          Format          |               Description                |
+===================+========+==========================+==========================================+
| target_state      | input  | State                    | | The target state that the workflow     |
|                   |        |                          | | object will jump to. It is supposed    |
|                   |        |                          | | to be a possible state in the future   |
|                   |        |                          | | of the workflow object                 |
+-------------------+--------+--------------------------+------------------------------------------+

.. toctree::
    :maxdepth: 2
