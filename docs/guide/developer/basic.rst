.. _developer_guide:


Basic Guide
===========

After :ref:`configuration <configuration>` we can now simply use it;  

.. code-highlight:: python

	from river.models.fields.state import StateField
  	class MyModel(models.Model):
    	my_state_field = StateField()

.. code-block:: python

    from river.models.fields.state import StateField

    class MyModel(models.Model):
        my_state_field = StateField()
        

``StateField`` is a model field defined in ``django-river``, which prepare everything for you. Whenever you put this field into a model object, the model converts into a workflow model.

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

Approvement Meta:
^^^^^^^^^^^^^^^^
These are approvement meta of transitions that describes which user permission or user group will be allowed to approve the transition. These are kind of template for approvements will be created for each object. An order can also be given here for the transition. This means, If you want to order approvement for a transition, you can define it. Assume **s1** and **s2** are our states and there is a transition defined between them and we have two approvement meta on this transition. They shall be for**permission1** and **permission2**. If you want object is on approval first **permission1** and after it is approved by permission1, then it is on approval the second permission which is **permission2**, you can do it with `djang-river` by defining order in this model.

Approvement:
^^^^^^^^^^^
There are state machines paths which is needed to be approved for every particular object. Approvements are generated on your model object creation by using `approvement meta`. This is whole path for the created object. Do not add or edit this model data unless you don't need specific objects editing like skiping, overriding permissions and groups.

Approvement Track:
""""""""""""""""""
In some scenarios, especially state machines contains circularity, approvements can be stated for multiple times. This is the model for the model of approvements. This is definite path of workflow for your objects.
    