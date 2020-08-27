.. _hooking_general_guide:

Statically Defined Hooks
=========================

Static hooks are for hooking up to a certain event by providing a function statically defined in the workspace rather than managing it on DB. Chanages with
static hooks require new deployments to be applied since there will be code changes. But it fits perfectly well if your workflow is programmatically created.

Please see :ref:`Class Level Hooking API` to create one for all objects in a workflow or see :ref:`Instance Level Hooking API` to create one for a specific object in a workflow
