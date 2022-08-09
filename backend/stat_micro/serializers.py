from rest_framework import serializers
from .models import *

class SecStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityStats
        fields = '__all__'