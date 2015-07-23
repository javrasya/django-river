from rest_framework import viewsets
from apps.riverio.models.object import Object

from apps.riverio.models.state import State
from apps.riverio.views.tokenized import TokenizedMixin

from apps.riverio.views.serializers.state import StateSerializer


__author__ = 'ahmetdal'


class ObjectViewSet(viewsets.ModelViewSet, TokenizedMixin):
    """
    An API which you can get or filter States.
    label -- State label to filter.
    """

    model = Object
    serializer_class = StateSerializer

    def get_queryset(self):
        ##TODO
        return State.objects.all()