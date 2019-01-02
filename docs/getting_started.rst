.. _getting-started:

Getting Started
===============
1. Install and enable it

   .. code:: bash

       pip install django-river

   .. code:: python

       INSTALLED_APPS=[
       ...
       river
       ...
       ]

2. Create your states as one of them will be your initial state (Look at :ref:`state-administration`.)
3. Create your transition approval metadata with authorized permissions and user groups along with their priority (Look at :ref:`transition-approval-meta-administration`.)
4. Create your first state machine in your model

    .. code:: python

        from django.db import models
        from river.models.fields.state import StateField

        class MyModel(models.Model):
            my_state_field = StateField()

5. Enjoy your ``django-river`` journey.

    .. code-block:: python

        my_model=MyModel.objects.get(....)
        
        my_model.river.my_state_field.approve(as_user=transactioner_user)
        my_model.river.my_state_field.approve(as_user=transactioner_user,next_state=State.objects.get(label='re-opened'))

        # and much more. Check the documentation

This is it. Whenever a model object is saved, it's state field will be initialized with the 
state is given at step-2 above by ``django-river``.

.. note:: 
    Make sure there is only one initial state picked in your workflow, so ``django-river`` can pick that one automatically 
    when a model object is created. All other workflow items will be created by ``django-river`` by object creations.