from rest_framework import serializers


__author__ = 'ahmetdal'


class ObjectRegistrationSerializer(serializers.Serializer):
    content_type_id = serializers.IntegerField()
    object_id = serializers.IntegerField()
    field_id = serializers.IntegerField()