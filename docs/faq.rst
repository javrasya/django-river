.. _faq:

FAQ
===

What does "supporting on-the-fly changes" mean?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It means that the changes require neither a code change nor a deployment.
In other words it is called as ``Dynamic Workflow``.

What are the advantages of dynamic workflows?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Ease of modifications on workflows. People most of the time lack of having
easily modifying workflow capability with their system. Especially when to often
workflow changes are needed. Adding up one more step, creating a callback function
right away and deleting them even for a specific workflow object when needed by
just modifying it in the Database is giving to much flexibility. It also doesn't
require any code knowledge to change a workflow as long as some user interfaces
are set up for those people.

What are the disadvantages of dynamic workflows?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Again, ease of modifications on workflows. Having too much freedom sometimes may
not be a good idea. Very critical workflows might need more attention and care
before they get modified. Even though having a workflow statically defined in the
code brings some bureaucracy, it might be good to have it to prevent accidental
modifications and to lessen human errors.

What are the differences between ``django-river`` and ``viewflow``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are different kind of workflow libraries for ``django``. It can be
working either with dynamically defined workflows or with statically defined
workflows. ``django-river`` is one of those that works with dynamically defined
workflows (what we call that it supports on-the-fly changes) where as ``viewflow``
is one of those that works with statically defined workflows in the code.

What are the differences between ``django-river`` and ``django-fsm``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are different kind of workflow libraries for ``django``. It can be
working either with dynamically defined workflows or with statically defined
workflows. ``django-river`` is one of those that works with dynamically defined
workflows (what we call that it supports on-the-fly changes) where as ``django-fsm``
is one of those that works with statically defined workflows in the code.

Can I have multiple initial states in a workflow?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. The way how ``django-river`` works is that, whenever one of your workflow
object is created, the state field of the workflow inside that object is set by
the initial field you specified. So it would be ambiguous to have more than one
initial state.

Can I have a workflow that circulates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. ``django-river`` allows that and as it circulates, ``django-river`` extends
the lifecycle of a particular workflow object with the circular part of it.

Is there a limit on how many states I can have in a workflow?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. You can have as many as you like.

Can I have an authorization rule consist of two user groups? (``Horizontal Authorization Rules``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. It functions like an or operator. One authorization rule
is defined with multiple user groups or permissions and anyone
who is any of the groups or who has any of the permissions defined
in that authorization rule can see and approve that transition.

Can I have two authorization rules for one transition and have one of them wait the other? (``Vertical Authorization Rules``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. ``django-river`` has some kind of a prioritization mechanism
between the authorization rules on the same transitions. One that is
with more priority will be able to be seen and approved before the one with
less priority on the same transitions. Let's say you have a workflow with a
transition which should be approved by a team leader before it bothers
the manager. That is so possible with ``django-river``.

Can I have two state fields in one ``Django`` model?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. The qualifier of a workflow for ``django-river`` is the model class and field name.
You can have as many workflow as you like in a ``Django`` model.

Can I have two workflow in parallel?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. The qualifier of a workflow for ``django-river`` is the model class and field name.
You can have as many workflow as you like in a ``Django`` model.

Can I have two workflow in different ``Django`` models?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Yes. The qualifier of a workflow for ``django-river`` is the model class and field name.
So it is possible to qualify yet another workflow with a different model class.


Does it support all the databases that are supported by ``Django``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Theoretically yes but it is only tested with ``sqlite3`` and all ``PostgreSQL`` versions.

What happens to the existing workflow object if I add a new transition to the workflow?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simply nothing. Existing workflow objects are not affected by the changes
on the workflow (Except the hooks). The way how ``django-river`` works is
that, it creates an isolated lifecycle for an object when it is created
out of it's workflow specification once and remain the same forever. So it
lives in it's world. It is very hard to predict what is gonna happen to the
existing objects. It requires more manual interference of the workflow owners
something like a migration process. But for the time being, we rather don't
touch the existing workflow objects due to the changes on the workflow.

Can I add a new hook on-the-fly?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The answer has ben yes since ``django-river`` version ``3.0.0``.

Can I delete an existing hook on-the-fly?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The answer has ben yes since ``django-river`` version ``3.0.0``.

Can I modify a the source code of the function that is used in the hooks on-the-fly?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The answer has ben yes since ``django-river`` version ``3.0.0``. ``django-river`` also
comes with an input component on the admin page that supports basic code highlighting.

Is there any delay for functions updates?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is none. It is applied immediately.

Can I use ``django-river`` with ``sqlalchemy``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The answer is no unless you can make ``Django`` work with ``sqlalchemy``.
``django-river`` uses ``Django``'s orm heavily. So it is probably not a
way to go.

What is the difference between ``Class API`` and ``Instance API``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``django-river`` provides two kinds of API. One which is for the object and one
which is for the class of the object. The ``Class API`` is the API that you can access
via the class whereas the ``Instance API`` is the API that you can access via the instance
or in other words via the workflow object. The APIs on both sides differ from each other
So don't expect to have the same function on both sides.

.. code:: python

   # Instance API
   from models import Shipping

   shipping_object = Shipping.objects.get(pk=1)
   shipping_object.river.shipping_status.approve(as_user=someone)


.. code:: python

   # Class API
   from models import Shipping

   Shipping.river.shipping_status.get_on_approval_objects(as_user=someone)

You can see all class api functions at `Class API`_
and all instance api functions at `Instance API`_.

What is the error ``'ClassWorkflowObject' object has no attribute 'approve'``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``approve`` is a function of `Instance API`_ not  a `Class API`_ one.


What is the error ``There is no available approval for the user.``?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It means the user that you are trying to approve with is not really authorized
to approve the next step of the transition. Catch the error and turn it to a
more user friendly error if you would like to warn your user about that.

How to reproduce before opening an issue?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``django-river`` has behavioral tests that are very easy to read and write. One can easily set up one
and see if everything is running as expected. Please look at other examples (that are the files with ``.feature`` postfix)
under ``features`` folder that you can get all the inspiration and create one for yourself before you open an issue
Then refer to your behavioral test to point out what is not function as expected to speed the process up for your own
sake. It is even better to name it with your issue number so we can persist it in the repository.

.. _`Class API`: https://django-river.readthedocs.io/en/latest/api/class.html
.. _`Instance API`: https://django-river.readthedocs.io/en/latest/api/instance.html

