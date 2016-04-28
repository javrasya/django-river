from river.models.proceeding import Proceeding
from river.models.proceeding_meta import ProceedingMeta
from river.models.state import State
from river.services.object import ObjectService
from river.services.proceeding import ProceedingService
from river.tests.base_test import BaseTestCase

__author__ = 'ahmetdal'


class test_ProceedingService(BaseTestCase):
    def test_get_proceedings_object_waiting_for_approval_without_skip(self):
        self.initialize_normal_scenario()

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field,
                                                                  [self.objects[0].my_field], user=self.user1)
        self.assertEqual(1, proceedings.count())

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field,
                                                                  [self.objects[0].my_field], user=self.user2)
        self.assertEqual(0, proceedings.count())

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field,
                                                                  [self.objects[0].my_field], user=self.user3)
        self.assertEqual(0, proceedings.count())

        proceedings = ProceedingService.get_available_proceedings(self.objects[0], self.field,
                                                                  [self.objects[0].my_field], user=self.user4)
        self.assertEqual(0, proceedings.count())

    def test_get_next_proceedings(self):
        self.initialize_normal_scenario()

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(9, proceedings.count())

        self.objects[0].proceed(self.user1)

        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(8, proceedings.count())

        self.objects[0].proceed(self.user2)

        # Two proceedings exist on same level
        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(7, proceedings.count())

        self.objects[0].proceed(self.user3)

        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(6, proceedings.count())

        self.objects[0].proceed(self.user4, next_state=State.objects.get(label='s4'))
        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(2, proceedings.count())

        self.objects[0].proceed(self.user4, next_state=State.objects.get(label='s4.1'))
        proceedings = ProceedingService.get_next_proceedings(self.objects[0], self.field)
        self.assertEqual(0, proceedings.count())

    def test_get_proceedings_object_waiting_for_approval_with_skip(self):
        self.initialize_normal_scenario()

        ObjectService.register_object(self.objects[0], self.field)
        ObjectService.register_object(self.objects[1], self.field)

        proceedings = self.objects[1].get_available_proceedings(self.user1)
        self.assertEqual(1, proceedings.count())
        self.assertEqual(State.objects.get(label='s2'), proceedings[0].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s2')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field,
                                                                  [self.objects[1].my_field], user=self.user2)
        self.assertEqual(1, proceedings.count())
        self.assertEqual(State.objects.get(label='s3'), proceedings[0].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s3')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field,
                                                                  [self.objects[1].my_field], user=self.user4)
        self.assertEqual(2, proceedings.count())
        self.assertEqual(State.objects.get(label='s4'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5'), proceedings[1].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field,
                                                                  [self.objects[1].my_field], user=self.user4)
        self.assertEqual(3, proceedings.count())
        self.assertEqual(State.objects.get(label='s5'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.1'), proceedings[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), proceedings[2].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s4')
        ).update(skip=False)
        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state=State.objects.get(label='s5')
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field,
                                                                  [self.objects[1].my_field], user=self.user4)
        self.assertEqual(3, proceedings.count())
        self.assertEqual(State.objects.get(label='s4'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), proceedings[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), proceedings[2].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4', 's5'])
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field,
                                                                  [self.objects[1].my_field], user=self.user4)
        self.assertEqual(4, proceedings.count())
        self.assertEqual(State.objects.get(label='s4.1'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s4.2'), proceedings[1].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.1'), proceedings[2].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), proceedings[3].meta.transition.destination_state)

        Proceeding.objects.filter(
            field=self.field,
            workflow_object=self.objects[1],
            meta__transition__destination_state__in=State.objects.filter(label__in=['s4.1', 's5.1'])
        ).update(skip=True)

        proceedings = ProceedingService.get_available_proceedings(self.objects[1], self.field,
                                                                  [self.objects[1].my_field], user=self.user4)
        self.assertEqual(2, proceedings.count())
        self.assertEqual(State.objects.get(label='s4.2'), proceedings[0].meta.transition.destination_state)
        self.assertEqual(State.objects.get(label='s5.2'), proceedings[1].meta.transition.destination_state)

    def test_cycle_proceedings(self):
        self.initialize_circular_scenario()

        ObjectService.register_object(self.objects[0], self.field)

        # No Cycle
        self.assertFalse(ProceedingService.cycle_proceedings(self.objects[0], self.field))
        self.objects[0].proceed(user=self.user1, next_state=self.in_progress_state, god_mod=True)
        self.assertEqual(5, Proceeding.objects.filter(object_id=self.objects[0].pk).count())

        # No Cycle
        self.assertFalse(ProceedingService.cycle_proceedings(self.objects[0], self.field))
        self.objects[0].proceed(user=self.user2, next_state=self.resolved_state, god_mod=True)
        self.assertEqual(5, Proceeding.objects.filter(object_id=self.objects[0].pk).count())

        # State is re-opened and cycle is detected. Transition in-progress to resolved proceeding is cloned
        self.assertFalse(ProceedingService.cycle_proceedings(self.objects[0], self.field))
        self.objects[0].proceed(user=self.user3, next_state=self.re_opened_state, god_mod=True)
        self.assertEqual(6, Proceeding.objects.filter(object_id=self.objects[0].pk).count())
        self.assertEqual(ProceedingMeta.objects.get(transition__source_state=self.in_progress_state,
                                                    transition__destination_state=self.resolved_state),
                         Proceeding.objects.filter(object_id=self.objects[0].pk).latest('date_created').meta)

        # There will be no cycling even if the method is invoked. Because cycling is done in proceeding.
        self.assertFalse(ProceedingService.cycle_proceedings(self.objects[0], self.field))
        self.assertEqual(6, Proceeding.objects.filter(object_id=self.objects[0].pk).count())

        # State is in-progress and cycle is detected. Transition resolved to re-opened proceeding is cloned
        self.objects[0].proceed(user=self.user3, next_state=self.in_progress_state, god_mod=True)
        self.assertEqual(7, Proceeding.objects.filter(object_id=self.objects[0].pk).count())
        self.assertEqual(ProceedingMeta.objects.get(transition__source_state=self.resolved_state,
                                                    transition__destination_state=self.re_opened_state),
                         Proceeding.objects.filter(object_id=self.objects[0].pk).latest('date_created').meta)

        # State is resolved and cycle is detected. Transition re-opened to in-progress proceeding is cloned
        self.objects[0].proceed(user=self.user3, next_state=self.resolved_state, god_mod=True)
        self.assertEqual(8, Proceeding.objects.filter(object_id=self.objects[0].pk).count())
        self.assertEqual(ProceedingMeta.objects.get(transition__source_state=self.re_opened_state,
                                                    transition__destination_state=self.in_progress_state),
                         Proceeding.objects.filter(object_id=self.objects[0].pk).latest('date_created').meta)

        # State is re-opened and cycle is detected. Transition  in-progress to resolved proceeding is cloned
        self.assertFalse(ProceedingService.cycle_proceedings(self.objects[0], self.field))
        self.objects[0].proceed(user=self.user3, next_state=self.re_opened_state, god_mod=True)
        self.assertEqual(9, Proceeding.objects.filter(object_id=self.objects[0].pk).count())
        self.assertEqual(ProceedingMeta.objects.get(transition__source_state=self.in_progress_state,
                                                    transition__destination_state=self.resolved_state),
                         Proceeding.objects.filter(object_id=self.objects[0].pk).latest('date_created').meta)

        # State is in-progress and cycle is detected. Transition resolved to re-opened proceeding is cloned
        self.objects[0].proceed(user=self.user3, next_state=self.in_progress_state, god_mod=True)
        self.assertEqual(10, Proceeding.objects.filter(object_id=self.objects[0].pk).count())
        self.assertEqual(ProceedingMeta.objects.get(transition__source_state=self.resolved_state,
                                                    transition__destination_state=self.re_opened_state),
                         Proceeding.objects.filter(object_id=self.objects[0].pk).latest('date_created').meta)

        # State is resolved and cycle is detected. Transition re-opened to in-progress proceeding is cloned
        self.objects[0].proceed(user=self.user3, next_state=self.resolved_state, god_mod=True)
        self.assertEqual(11, Proceeding.objects.filter(object_id=self.objects[0].pk).count())
        self.assertEqual(ProceedingMeta.objects.get(transition__source_state=self.re_opened_state,
                                                    transition__destination_state=self.in_progress_state),
                         Proceeding.objects.filter(object_id=self.objects[0].pk).latest('date_created').meta)

        # No Cycle for closed state.
        self.objects[0].proceed(user=self.user4, next_state=self.closed_state, god_mod=True)
        self.assertEqual(11, Proceeding.objects.filter(object_id=self.objects[0].pk).count())
