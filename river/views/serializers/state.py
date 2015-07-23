from rest_framework import serializers
from apps.riverio.models.state import State

__author__ = 'ahmetdal'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State