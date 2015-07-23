from rest_framework import serializers
from apps.riverio.models.application import Application


__author__ = 'ahmetdal'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('id', 'name')