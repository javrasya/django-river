from rest_framework import serializers


__author__ = 'ahmetdal'



class ObjectCountOnApprovalSerializer(serializers.Serializer):
    count = serializers.IntegerField()