from itertools import chain, combinations

import six


def powerset(iterable):
    xs = list(iterable)
    # note we return an iterator rather than a list
    return chain.from_iterable(combinations(xs, n) for n in range(len(xs) + 1))


def _build_hash_key_to_put(**object_identifiers):
    identifiers = [key + str(value) for key, value in object_identifiers.items() if value]
    return six.moves.reduce(lambda hash_key, identifier: hash_key + identifier, identifiers, "")


def _build_hash_keys_to_get(**object_identifiers):
    identifiers = [key + str(value) for key, value in object_identifiers.items() if value]
    return ["".join(parts) for parts in powerset(identifiers) if parts]


def _hook_it_up(callback_function, callback_store, **identifiers):
    hash_key = _build_hash_key_to_put(**identifiers)
    callback_store[hash_key] = callback_function


def _get_callbacks(callback_store, **identifiers):
    hash_keys = _build_hash_keys_to_get(**identifiers)
    return [callback_store[hash_key] for hash_key in hash_keys if hash_key in callback_store]


class StaticHookRegistry(object):
    def __init__(self):
        self.pre_approve_callbacks = {}
        self.post_approve_callbacks = {}
        self.pre_transit_callbacks = {}
        self.post_transit_callbacks = {}
        self.pre_complete_callbacks = {}
        self.post_complete_callbacks = {}

    def list_on_pre_approve_callbacks(self, workflow, transition_approval_meta, workflow_object, transition_approval):
        return _get_callbacks(
            self.pre_approve_callbacks,
            workflow=workflow.pk,
            transition_approval_meta=transition_approval_meta.pk,
            workflow_object=workflow_object.pk,
            transition_approval=transition_approval.pk
        )

    def list_on_post_approve_callbacks(self, workflow, transition_approval_meta, workflow_object, transition_approval):
        return _get_callbacks(
            self.post_approve_callbacks,
            workflow=workflow.pk,
            transition_approval_meta=transition_approval_meta.pk,
            workflow_object=workflow_object.pk,
            transition_approval=transition_approval.pk
        )

    def list_on_pre_transition_callbacks(self, workflow, transition_meta, workflow_object, transition):
        return _get_callbacks(
            self.pre_transit_callbacks,
            workflow=workflow.pk,
            transition_meta=transition_meta.pk,
            workflow_object=workflow_object.pk,
            transition=transition.pk
        )

    def list_on_post_transition_callbacks(self, workflow, transition_meta, workflow_object, transition):
        return _get_callbacks(
            self.post_transit_callbacks,
            workflow=workflow.pk,
            transition_meta=transition_meta.pk,
            workflow_object=workflow_object.pk,
            transition=transition.pk
        )

    def list_on_pre_complete_callbacks(self, workflow, workflow_object):
        return _get_callbacks(
            self.pre_complete_callbacks,
            workflow=workflow.pk,
            workflow_object=workflow_object.pk,
        )

    def list_on_post_complete_callbacks(self, workflow, workflow_object):
        return _get_callbacks(
            self.post_complete_callbacks,
            workflow=workflow.pk,
            workflow_object=workflow_object.pk,
        )

    def on_pre_approve(self, callback_function, workflow, transition_approval_meta, workflow_object=None, transition_approval=None):
        _hook_it_up(
            callback_function,
            self.pre_approve_callbacks,
            workflow=workflow.pk,
            transition_approval_meta=transition_approval_meta.pk,
            workflow_object=workflow_object.pk if workflow_object else None,
            transition_approval=transition_approval.pk if transition_approval else None
        )

    def on_post_approve(self, callback_function, workflow, transition_approval_meta, workflow_object=None, transition_approval=None):
        _hook_it_up(
            callback_function,
            self.post_approve_callbacks,
            workflow=workflow.pk,
            transition_approval_meta=transition_approval_meta.pk,
            workflow_object=workflow_object.pk if workflow_object else None,
            transition_approval=transition_approval.pk if transition_approval else None
        )

    def on_pre_transition(self, callback_function, workflow, transition_meta, workflow_object=None, transition=None):
        _hook_it_up(
            callback_function,
            self.pre_transit_callbacks,
            workflow=workflow.pk,
            transition_meta=transition_meta.pk,
            workflow_object=workflow_object.pk if workflow_object else None,
            transition=transition.pk if transition else None
        )

    def on_post_transition(self, callback_function, workflow, transition_meta, workflow_object=None, transition=None):
        _hook_it_up(
            callback_function,
            self.post_transit_callbacks,
            workflow=workflow.pk,
            transition_meta=transition_meta.pk,
            workflow_object=workflow_object.pk if workflow_object else None,
            transition=transition.pk if transition else None
        )

    def on_pre_complete(self, callback_function, workflow, workflow_object=None):
        _hook_it_up(callback_function, self.pre_complete_callbacks, workflow=workflow.pk, workflow_object=workflow_object.pk if workflow_object else None)

    def on_post_complete(self, callback_function, workflow, workflow_object=None):
        _hook_it_up(callback_function, self.post_complete_callbacks, workflow=workflow.pk, workflow_object=workflow_object.pk if workflow_object else None)


static_hook_registry = StaticHookRegistry()
