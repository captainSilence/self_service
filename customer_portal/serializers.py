from dataclasses import field
from .models import NewSpeedRequest
from rest_framework import serializers

class NewSpeedRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewSpeedRequest
        fields = '__all__'
        

