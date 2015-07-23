from rest_framework import serializers

from tests.apps.riverio.apps.base.models.field import Field
from tests.apps.riverio.apps.web.models.serializers.application_serializer import ApplicationSerializer


__author__ = 'ahmetdal'


class FieldSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(many=False)

    class Meta:
        model = Field
        fields = ('id', 'label', 'description', 'application')