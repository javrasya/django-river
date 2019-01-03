.. _hooking_guide:

Hooking Guide
=============

Hooking is one of the powerful side of ``django-river``. It is basically allowing you to have some callback functions due to some 
circumtances like transitions or workflow completions.

How Should Callback Functions Look Like
---------------------------------------

You can register your callback function for some circumtances via ``django-river`` hooking feature. It can either be when a spesific
transition happend or when a workflow is complete for an object. Your callback functions should look like how ``django-river`` wants
them to be.

If you want to see how you can register your callback, you can take a look at either :ref:`instance_api_hooking_pre_transition` or 
:ref:`instance_api_hooking_post_transition`. 

.. _transition_callback_function:

Transition Callback Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code:: python

       def my_callback_function(workflow_object, field_name, transition_approval=None):
            print(f"A transition happened: {transition_approval.source_state} -> {transition_approval.destination_state} by user {transition_approval.transactioner}")

+---------------------+--------+--------------------+---------------------------------------------------------+
|      Paramters      |  Type  |       Format       |                       Description                       |
+=====================+========+====================+=========================================================+
| workflow_object     | args   | YourModel          | | The instance of your workflow model that has just     |
|                     |        |                    | | transited                                             |
+---------------------+--------+--------------------+---------------------------------------------------------+
| field_name          | args   | String             | | State field name of that model object in the workflow |
|                     |        |                    | | that the transition happened in                       |
+---------------------+--------+--------------------+---------------------------------------------------------+
| transition_approval | kwargs | TransitionApproval | | The transition approval has just been approved right  |
|                     |        |                    | | before this transition happened. You can access the   |
|                     |        |                    | | transactioner user, source and destination states and |
|                     |        |                    | | many more within transition approval. For more detail |
|                     |        |                    | | look at TransitionApproval model source               |
+---------------------+--------+--------------------+---------------------------------------------------------+

.. _on_complete_callback_function:

On Complete Callback Function
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. code:: python

       def my_callback_function(workflow_object, field_name):
            print(f"The workflow is completed for workflow object {workflow_object} and field {field_name}")

+---------------------+--------+--------------------+---------------------------------------------------------+
|      Paramters      |  Type  |       Format       |                       Description                       |
+=====================+========+====================+=========================================================+
| workflow_object     | args   | YourModel          | | The instance of your workflow model whose workflow    |
|                     |        |                    | | has just been completed                               |
+---------------------+--------+--------------------+---------------------------------------------------------+
| field_name          | args   | String             | | State field name of that model object in the workflow |
|                     |        |                    | | that is completed                                     |
+---------------------+--------+--------------------+---------------------------------------------------------+

    
Hooking Backends
----------------

Hooking needs to have a mechanism to manage all the registered callbacks even in multi-process situations properly. This is a part where
you can use different types of hooking backends either the built-in ones or the ones that you may want to come up with on your own.

DatabaseHookingBackend
~~~~~~~~~~~~~~~~~~~~~~

This is the default hooking backend that keeps all the registered in the persistent databsase. Django applicaitons are usually running as 
multi-process on production and consequently ``django-river`` will call your callback functions multiple times in different processes with 
``MemoryHookingBackend``. You may want to have your callback functions being called only at once and this is what ``DatabaseHookingBackend`` is
for.

   .. code:: python

       .
       RIVER_HOOKING_BACKEND = {
            'backend':'river.hooking.backends.memory.DatabaseHookingBackend',
            'config' : {}
       }
       .

MemoryHookingBackend
~~~~~~~~~~~~~~~~~~~~

This is the hooking backend that keeps all the registered callbacks in memory and it is for development and test purposes. Since it is in memory
and not shared, it is not good for multi-process situation. When your object is saved in one instance where you register your callback
, but finalized in the workflow in another, your callback completion callback function will never be invoked for instance.