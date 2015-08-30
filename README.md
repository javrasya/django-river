# Django River
[![Build Status](https://travis-ci.org/javrasya/django-river.svg)](https://travis-ci.org/javrasya/django-river) [![Coverage Status](https://coveralls.io/repos/javrasya/django-river/badge.svg?branch=master&service=github)](https://coveralls.io/github/javrasya/django-river?branch=master) [![Documentation Status](https://readthedocs.org/projects/django-river/badge/?version=latest)](https://readthedocs.org/projects/django-river/?badge=latest)


River is a open source workflow system for `Django` which support on the fly changes on every item in workflow instead of hardcoding states and transitions.

Main goal of developing this framework is **to be able to edit any workflow item on the fly.** This means, all elements in workflow like states, transitions, user authorizations(permission), group authorization are editable. To do this, all data about the workflow item is persisted into DB. **Hence, they can be changed without touching the code and re-deploying your application.**

There is ordering aprovments for a transition functionality in `django-river`. It also provides skipping specific transition of a specific objects.

## Documentation

Online documentation is available at http://django-river.rtfd.org/.

## Installation

* Install it
```bash
pip install django-river
```

* Configure settings
```python
INSTALLED_APPS=[
	...
	river
	...
]
```
* Migrate your application
```bash
python manage.py migrate
```

* In your model class which will be processing in workflow;

```python
from django.db import models
from river.models.fields.state import StateField

class MyModel(models.Model):
    my_state_field = StateField()    
```

That's it. Whenever your new model object is saved, it's state field will be initialized according to given meta data about workflow. To know how to do your workflow confirmation(states, transitions, permissions etc.), see the next part.


## Usage for End User

1. Define your states.
2. Define your state transitions.
3. Define your approvement meta which contains permissions and groups authorization for transitions. Approvement order is also given here.

We are now ready to workflowing :)

Whenever an object of MyModel is inserted in your system, all its workflow initialization is done by `django-river`.

## Usage for Developer

###Signals:
**`pre_transition`**: it is fired before any transition occured.

| Args          		| Description                           |
| ----------------- |---------------------------------------|
| workflow_object	| Your object on transition             |
| field      			| Field which you registered object for |
| source_state 		| Transition source state object        |
| destination_state | Transition destination state object   |
| appovement 			| Approvement object                    |

**`post_transition`**: it is fired before any transition occured.

| Args          		| Description                           |
| ----------------- |---------------------------------------|
| workflow_object	| Your object on transition             |
| field      			| Field which you registered object for |
| source_state 		| Transition source state object        |
| destination_state | Transition destination state object   |
| appovement 			| Approvement object                    |


**`pre_approved`**: it is fired before any approvement occured. Transition does not have to be occured.

| Args          		| Description                           |
| ----------------- |---------------------------------------|
| workflow_object	| Your object approved                  |
| field      			| Field which you registered object for |
| appovement 			| Approvement object                    |
| track	 			| Approvement track object              |

**`post_approved`**: it is fired before any approvement occured. Transition does not have to be occured.

| Args          		| Description                           |
| ----------------- |---------------------------------------|
| workflow_object	| Your object approved                  |
| field      			| Field which you registered object for |
| appovement 			| Approvement object                    |
| track	 			| Approvement track object              |

**`pre_final`**: it is fired before any workflow is completed.

| Args          		| Description                           |
| ----------------- |---------------------------------------|
| workflow_object	| Your object on final                  |
| field      			| Field which you registered object for |

**`post_final`**: it is fired before any workflow is completed.

| Args          		| Description                           |
| ----------------- |---------------------------------------|
| workflow_object	| Your object on final                  |
| field      			| Field which you registered object for |

###Handlers:
Handlers are different from `django-river` signals. These are for spesific object, spesific source_state, spesific destination_state etc. It is fired when the condition is matched.

####`PreCompletedHandler`:
--
Before an object is on final state, if the condition is match; means object is suitable, it is fired;
```python
from river.handlers.completed import PreCompletedHandler

def handler(my_object,field,*args,**kwargs):
	do_something_with(object,field)

PreCompletedHandler.register(handler,my_object,'my_state_field')
```


**`register` method parameter**

| Args          		| Description                           |          |
| ----------------- |---------------------------------------|----------|
| workflow_object	| Your object                           | Required |
| field      			| Field which you registered object for | Required |

####`PostCompletedHandler`:
--
After an object is on final state, if the condition is match; means object is suitable, it is fired;
```python
from river.handlers.completed import PostCompletedHandler

def handler(my_object,field,*args,**kwargs):
	do_something_with(object,field)

PostCompletedHandler.register(handler,my_object,'my_state_field')
```


**`register` method parameter**

| Args          		| Description                           |          |
| ----------------- |---------------------------------------|----------|
| workflow_object	| Your object                           | Required |
| field      			| Field which you registered object for | Required |


####`PreTransitionHandler`:
--
Before any transition occurred, if the condition is match; means object, source_state,destination state are suitable, it is fired;
```python
from river.handlers.transition import PreTransitionHandler

def handler(my_object,field,*args,**kwargs):
	do_something_with(object,field)

PreTransitionHandler.register(handler,my_object,'my_state_field')
```


**`register` method parameter**

| Args          		| Description                           |          |
| ----------------- |---------------------------------------|----------|
| workflow_object	| Your object                           | Required |
| field      			| Field which you registered object for | Required |
| source_state      | Source state of the tranition         | Optional |
| desination_satte  | Destinatio state of the tranition     | Optional |

####`PostTransitionHandler`:
--
After any transition occurred, if the condition is match; means object, source_state,destination state are suitable, it is fired;
```python
from river.handlers.transition import PostTransitionHandler

def handler(my_object,field,*args,**kwargs):
	do_something_with(object,field)

PostTransitionHandler.register(handler,my_object,'my_state_field')
```



**`register` method parameter**

| Args          		| Description                           |          |
| ----------------- |---------------------------------------|----------|
| workflow_object	| Your object                           | Required |
| field      			| Field which you registered object for | Required |
| source_state      | Source state of the tranition         | Optional |
| desination_satte  | Destinatio state of the tranition     | Optional |


##Models:

####States: 
Indicates states in your state machine.

####Transitions: 
These are transition between your states. **There must be only one initial state** which is in a transition as destination state but no source state to make `django-river` find it on object creation.

####Approvement Meta: 
These are approvement meta of transitions that describes which user permission or user group will be allowed to approve the transition. These are kind of template for approvements will be created for each object. An order can also be given here for the transition. This means, If you want to order approvement for a transition, you can define it. Assume **s1** and **s2** are our states and there is a transition defined between them and we have two approvement meta on this transition. They shall be for**permission1** and **permission2**. If you want object is on approval first **permission1** and after it is approved by permission1, then it is on approval the second permission which is **permission2**, you can do it with `djang-river` by defining order in this model.

####Approvement
There are state machines paths which is needed to be approved for every particular object. Approvements are generated on your model object creation by using `approvement meta`. This is whole path for the created object. Do not add or edit this model data unless you don't need specific objects editing like skiping, overriding permissions and groups.
