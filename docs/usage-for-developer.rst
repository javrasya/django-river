.. _usage_for_developer:

Usage(Developer)
================

After :ref:`configuration <configuration>` we can now simply use it;  

.. code-block:: python

	from river.models.fields.state import StateField
  	class MyModel(models.Model):
    	my_state_field = StateField() 
 

.. note::
   If you 