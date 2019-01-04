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

3. Create your first state machine in your model

    .. code:: python

        from django.db import models
        from river.models.fields.state import StateField

        class MyModel(models.Model):
            my_state_field = StateField()

3. Create your states as one of them will be your initial state on the admin page (Look at :ref:`state-administration`.)
4. Create your transition approval metadata with your model (``MyModel`` - ``my_state_field``) information and authorization rules along with their priority on the admin page (Look at :ref:`transition-approval-meta-administration`.)
5. Enjoy your ``django-river`` journey.

    .. code-block:: python

        my_model=MyModel.objects.get(....)
        
        my_model.river.my_state_field.approve(as_user=transactioner_user)
        my_model.river.my_state_field.approve(as_user=transactioner_user,next_state=State.objects.get(label='re-opened'))

        # and much more. Check the documentation


.. note::
    Whenever a model object is saved, it's state field will be initialized with the
    state is given at step-3 above by ``django-river``.

.. note:: 
    Make sure that there is only one initial state defined in your workflow, so that ``django-river`` can pick that one automatically
    when a model object is created. All other workflow items will be managed by ``django-river`` after object creations.