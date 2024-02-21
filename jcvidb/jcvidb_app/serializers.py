from rest_framework import serializers
from .models import Proteomic


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proteomic
        fields = ('freeGeneSet', 'PGAN', 'locusTag', 'createdBy', 'essentiality', 'transporters', 'coverage',
                  'attachment', 'creationDate')
