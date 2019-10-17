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

.. toctree::
    :maxdepth: 2