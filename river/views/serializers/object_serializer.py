from rest_framework import serializers

from apps.riverio.models.object import Object


__author__ = 'ahmetdal'


class ObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Object

