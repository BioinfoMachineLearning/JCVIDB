from rest_framework import serializers
from .models import Basic_data


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basic_data
        fields = ('funding',  'details', 'type','references',
                  'attachment', 'creationDate','type')
