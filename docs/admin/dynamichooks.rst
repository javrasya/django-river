.. _transition-meta-administration:

Dynamic Hook Administration
===========================

OnTransitHook
-------------
+---------------------------+------------+----------+--------------------+-------------------------------------------+
|           Field           |  Default   | Optional |       Format       |                Description                |
+===========================+============+==========+====================+===========================================+
| workflow                  |            |          |  Workflow          | | Your model class along with the field   |
|                           |            |          |                    | | that you want to use this transition    |
|                           |            | False    |                    | | approval meta for. ``django-river``     |
|                           |            |          |                    | | will list all the possible model and    |
|                           |            |          |                    | | fields you can pick on the admin page   |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| callback_function         |            | False    | Function           | | Call back function model object that    |
|                           |            |          |                    | | contains the name and the body          |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| transition_meta           |            | False    | TransitionMeta     | | The meta of the transition that the     |
|                           |            |          |                    | | callback function will be executed      |
|                           |            |          |                    | | for                                     |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| hook_type                 |            | False    | BEFORE or AFTER    | | When the call back should be executed   |
+---------------------------+------------+----------+--------------------+-------------------------------------------+
| workflow_object           | None       | True     | ModelWithStateField| | Your model object. This field is        |
|                           |            |          |                    | | When it is provided, the call back for  |
|                           |            |          |                    | | the transition will only be executed for|
|                           |            |          |                    | | the given model object                  |
+---------------------------+------------+----------+--------------------+-------------------------------------------+


OnApprovedHook
--------------
+---------------------------+------------+----------+--------------------+--------------------------------------------------+
|           Field           |  Default   | Optional |       Format       |                Description                       |
+===========================+============+==========+====================+==================================================+
| workflow                  |            |          |  Workflow                 | | Your model class along with the field   |
|                           |            |          |                           | | that you want to use this transition    |
|                           |            | False    |                           | | approval meta for. ``django-river``     |
|                           |            |          |                           | | will list all the possible model and    |
|                           |            |          |                           | | fields you can pick on the admin page   |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
| callback_function         |            | False    | Function                  | | Call back function model object that    |
|                           |            |          |                           | | contains the name and the body          |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
| transition_approval_meta  |            | False    | TransitionApprovalMeta    | | The meta of the approval that the       |
|                           |            |          |                           | | callback function will be executed      |
|                           |            |          |                           | | for                                     |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
| hook_type                 |            | False    | BEFORE or AFTER           | | When the call back should be executed   |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
| workflow_object           | None       | True     | ModelWithStateField       | | Your model object. This field is        |
|                           |            |          |                           | | When it is provided, the call back for  |
|                           |            |          |                           | | the transition will only be executed for|
|                           |            |          |                           | | the given model object                  |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+


OnCompleteHook
--------------
+---------------------------+------------+----------+--------------------+--------------------------------------------------+
|           Field           |  Default   | Optional |       Format       |                Description                       |
+===========================+============+==========+====================+==================================================+
| workflow                  |            |          |  Workflow                 | | Your model class along with the field   |
|                           |            |          |                           | | that you want to use this transition    |
|                           |            | False    |                           | | approval meta for. ``django-river``     |
|                           |            |          |                           | | will list all the possible model and    |
|                           |            |          |                           | | fields you can pick on the admin page   |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
| callback_function         |            | False    | Function                  | | Call back function model object that    |
|                           |            |          |                           | | contains the name and the body          |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
| hook_type                 |            | False    | BEFORE or AFTER           | | When the call back should be executed   |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+
| workflow_object           | None       | True     | ModelWithStateField       | | Your model object. This field is        |
|                           |            |          |                           | | When it is provided, the call back for  |
|                           |            |          |                           | | the transition will only be executed for|
|                           |            |          |                           | | the given model object                  |
+---------------------------+------------+----------+---------------------------+-------------------------------------------+

.. toctree::
    :maxdepth: 2