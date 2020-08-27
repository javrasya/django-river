.. _transition-meta-administration:

Transition Meta Administration
==============================
+---------------------------+------------+----------+--------------------+-------------------------------------------+
|           Field           |  Default   | Optional |       Format       |                Description                |
+===========================+============+==========+====================+===========================================+
| workflow                  |            | False    | Workflow           | | Your model class along with the field   |
|                           |            |          |                    | | that you want to use this transition    |
|                           |            |          |                    | | approval meta for. ``django-river``     |
|                           |            |          |                    | | will list all the possible model and    |
|                           |            |          |                    | | fields you can pick on the admin page   |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| source_state              |            | False    | State              | | Source state of the transition          |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| destination_state         |            | False    | State              | | Destination state of the transition     |
+---------------------------+------------+----------+--------------------+-------------------------------------------+


.. toctree::
    :maxdepth: 2