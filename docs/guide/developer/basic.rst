.. _developer_guide:


Basic Guide
===========

After :ref:`configuration <configuration>` we can now simply use it;  

.. code-block:: python
	
    from river.models.fields.state import StateField
    class MyModel(models.Model):
        my_state_field = StateField()

``StateField`` is a model field defined in ``django-river``, which prepare everything for you. Whenever you put this field into a model object, the model converts into a workflow model. 

.. code-block:: python

    my_model=MyModel.objects.get(....)
    
    my_model.proceed(transactioner_user)
    my_model.proceed(transactioner_user,next_state=State.objects.get(label='re-opened'))
        

``proceed`` methods is injected into your model objects. The object will be in next state if the given user is authorized to do that transaction. When there is two destination states available from current state, ``next_state`` must be given to the function. If there is only one state can be at, no needs to give it; ``django-river`` will detect it.

.. note::
   If you want to know more about ``StateField`` in advanced model, look at :ref:`advance <advance>`



Models in ``django-river``
--------------------------
States:
^^^^^^^
Indicates states in your state machine.

Transitions:
^^^^^^^^^^^^
These are transition between your states. **There must be only one initial state** which is in a transition as destionation state but no source state to make `django-river` find it on object creation.

Proceeding Meta:
^^^^^^^^^^^^^^^^^
These are proceeding meta of transitions that describes which user permission or user group will be allowed to proceed the transition. These are kind of template for proceedings will be created for each object. An order can also be given here for the transition. This means, If you want to order proceeding for a transition, you can define it. Assume **s1** and **s2** are our states and there is a transition defined between them and we have two proceeding meta on this transition. They shall be for**permission1** and **permission2**. If you want object is on approval first **permission1** and after it is proceeded by permission1, then it is on approval the second permission which is **permission2**, you can do it with `djang-river` by defining order in this model.

Proceeding:
^^^^^^^^^^^^
There are state machines paths which is needed to be proceeded for every particular object. Proceedings are generated on your model object creation by using `proceeding meta`. This is whole path for the created object. Do not add or edit this model data unless you don't need specific objects editing like skiping, overriding permissions and groups.


Workflow Manager :
------------------
``django-river`` contains a model manager provides some methods about workflow;

.. code-block:: python

    from django.db import models
    from river.models.fields.state import StateField
    from river.models.managers.workflow_object import WorkflowObjectManager

    class MyModel(models.Model):
        my_state_field = StateField()

        objects = WorkflowObjectManager()


    >>> MyModel.objects.get_objects_waiting_for_approval(current_user)
    # Will give you your model instance objects which is waiting for approval by current user by considering his/her authorization rules.

    >>> MyModel.objects.get_object_count_waiting_for_approval(current_user)
    # Will give you count of your model instance objects which is waiting for approval by current user by considering his/her authorization rules. This can be used to show a badge contains a count on main screen for each user whether there are some objects waiting for approval.