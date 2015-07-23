from rest_framework import serializers


__author__ = 'ahmetdal'


class IsUserAuthorizedSerializer(serializers.Serializer):
    is_authorized = serializers.BooleanField(default=False)