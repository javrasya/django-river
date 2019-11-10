.. _transition-approval-meta-administration:

Transition Approval Meta Administration
=======================================
+---------------------------+------------+----------+--------------------+-------------------------------------------+
|           Field           |  Default   | Optional |       Format       |                Description                |
+===========================+============+==========+====================+===========================================+
| workflow                  |            |          | | Choice           | | Your model class along with the field   |
|                           |            |          | | of               | | that you want to use this transition    |
|                           |            | False    | | Strings          | | approval meta for. ``django-river``     |
|                           |            |          |                    | | will list all the possible model and    |
|                           |            |          |                    | | fields you can pick on the admin page   |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| transition_meta           |            | False    | TransitionMete     | | Transition information that contains    |
|                           |            |          |                    | | source and destination states           |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| permissions               | Empty List | True     | List<Permission>   | | List of permissions which will be       |
|                           |            |          |                    | | authorized to approve this              |
|                           |            |          |                    | | transition                              |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| groups                    | Empty List | True     | List<UserGroup>    | | List of use groups which will be        |
|                           |            |          |                    | | authorized to approve this              |
|                           |            |          |                    | | transition                              |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| priority                  | 0          | False    | Number             | | The priority of the transition          |
|                           |            |          |                    | | approval. Since there can be more       |
|                           |            |          |                    | | than one transition approval to         |
|                           |            |          |                    | | make that transition which means        |
|                           |            |          |                    | | that some users should approve          |
|                           |            |          |                    | | before some other users can approve     |
|                           |            |          |                    | | the same transition. The closer to      |
|                           |            |          |                    | | zero, the more priort the transition    |
|                           |            |          |                    | | approval is.                            |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| action_text (Depcrecated) |            | True     | String             | | An action text for this transition      |
|                           |            |          |                    | | like, ``Open``, ``Close``. If this      |
|                           |            |          |                    | | is not specified, than ``django-river`` |
|                           |            |          |                    | | will pick something like                |
|                           |            |          |                    | | ``source_state->destination_state``     |
+---------------------------+------------+----------+--------------------+-------------------------------------------+


.. toctree::
    :maxdepth: 2
    
