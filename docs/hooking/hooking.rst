.. _hooking_guide:

Hook it Up
==========

The hookings in ``django-river`` can be created both specifically for a workflow object or for a whole workflow. ``django-river`` comes with some model objects and admin interfaces which you can use
to create the hooks.

* To create one for whole workflow regardless of what the workflow object is, go to

    * ``/admin/river/onapprovedhook/`` to hook up to an approval
    * ``/admin/river/ontransithook/`` to hook up to a transition
    * ``/admin/river/oncompletehook/`` to hook up to the completion of the workflow

* To create one for a specific workflow object you should use the admin interface for the workflow object itself. One amazing feature of ``django-river`` is now that
it creates a default admin interface with the hookings for your workflow model class. If you have already defined one, ``django-river`` enriches your already defined
admin with the hooking section. It is default disabled. To enable it just define ``RIVER_INJECT_MODEL_ADMIN`` to be ``True`` in the ``settings.py``.


**Note:** They can programmatically be created as well since they are model objects. If it is needed to be at workflow level, just don't provide the workflow object column. If it is needed
to be for a specific workflow object then provide it.

Here are the list of hook models;

* OnApprovedHook
* OnTransitHook
* OnCompleteHook
