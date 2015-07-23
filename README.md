# Django River
[![Build Status](https://travis-ci.org/javrasya/django-river.svg)](https://travis-ci.org/javrasya/django-river) [![Coverage Status](https://coveralls.io/repos/github/javrasya/django-river/badge.svg?branch=master)](https://coveralls.io/github/javrasya/django-river?branch=master)

River is a open source workflow system for `Django` which support on the fly changes on every item in workflow instead of hardcoding states and transitions.

Main goal of developing this framework is **to be able to edit any workflow item on the fly.** This means, all elements in workflow like states, transitions, user authorizations(permission), group authorization are editable. To do this, all data about the workflow item is persisted into DB. **Hence, they can be change without touching the code and re-deploying your application.**

There is ordering aprovments for a transition functionality in `django-river`. It also provides skipping specific transition of a specific objects.


## Installation

* Install it
```bash
pip install git+https://github.com/javrasya/django-river.git
```

* Configure settings
```python
INSTALLED_APP=[
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

That's it. Whenever your new model object is saved, it'll be state field will be initialized according to given meta data about workflow. To know how to do your workflow confirmation(states, transitions, permissions etc.), see the next part.


## Usage	

1. Define your states.
2. Define your state transitions.
3. Define your approvement meta which contains permissions and groups authorization for transitions. Approvement order is also given here.

We are now ready to workflowing :)

Whenever an object of MyModel is inserted in your system, all its workflow initialization is done by `django-river`.


##Models:

####States: 
Indicates states in your state machine.

####Transitions: 
These are transition between your states. **There must be only one initial state** which is in a transition as destionation state but no source state to make `django-river` find it on object creation.

####Approvement Meta: 
These are approvement meta of transitions that describes which user permission or user group will be allowed to approve the transition. These are kind of template for approvements will be created for each object. An order can also be given here for the transition. This means, If you want to order approvement for a transition, you can define it. Assume **s1** and **s2** are our states and there is a transition defined between them and we have two approvement meta on this transition. They shall be for**permission1** and **permission2**. If you want object is on approval first **permission1** and after it is approved by permission1, then it is on approval the second permission which is **permission2**, you can do it with `djang-river` by defining order in this model.

####Approvement
There are state machines paths which is needed to be approved for every particular object. Approvements are generated on your model object creation by using `approvement meta`. This is whole path for the created object. Do not add or edit this model data unless you don't need specific objects editing like skiping, overriding permissions and groups.