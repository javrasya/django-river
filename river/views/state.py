from rest_framework import viewsets

from apps.riverio.models.state import State
from apps.riverio.views.serializers.state import StateSerializer
from apps.riverio.views.tokenized import TokenizedMixin


__author__ = 'ahmetdal'


class StateViewSet(viewsets.ReadOnlyModelViewSet, TokenizedMixin):
    """
    An API which you can get or filter States.
    label -- State label to filter.
    """

    model = State
    serializer_class = StateSerializer


    def filter_queryset(self, queryset):
        return super(StateViewSet, self).filter_queryset(queryset).filter(**self.request.GET.dict())

    def get_queryset(self):
        ##TODO
        return State.objects.all()