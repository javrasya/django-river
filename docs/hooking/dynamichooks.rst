.. _hooking_general_guide:

Dynamically Defined Hooks
=========================

``django-river`` allows to create hooks for certain type of events dynamically which also fits well in django-river's main idea which is allowing
on the fly changes without a new deployment.

* It can be created for whole objects in a workflow or a specific objects. One amazing feature of ``django-river`` is now that
it creates a default admin interface with the hookings for your workflow model class. If you have already had your own admin page for your mode
, ``django-river`` enriches it with the hooking section. It is disabled by default. To enable it just define ``RIVER_INJECT_MODEL_ADMIN``
to be ``True`` in the ``settings.py``.

Please see :ref:`Dynamic Hook Administration` to get he inspiration what the fields mean and you can programmatically create them by yourself as well.

**Note:** Be careful with using dynamically define hooks feature since what ever defined in the given dynamically created python code blocks will
be executed without any safe guard. It is recommended to run your Django app with a restricted system user to avoid accidents.

**Note:** This feature is only recommended for admin purposes and it is not for end-users to avoid unexpected injections.

Here are the list of hook models;

* OnApprovedHook
* OnTransitHook
* OnCompleteHook


Example
-------

   .. code:: python

       OnTransitHook.objects.create(
            workflow=workflow,
            callback_function=callback_function_model_object,
            transition_meta=transition_meta,
            transition=transition,
            hook_type=BEFORE,
            workflow_object=workflow_object,
       )

       OnTransitHook.objects.create(
            workflow=workflow,
            callback_function=callback_function_model_object,
            transition_meta=transition_meta,
            transition=transition,
            hook_type=BEFORE,
            workflow_object=workflow_object,
       )

.. toctree::
    :maxdepth: 2