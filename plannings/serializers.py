from rest_framework import serializers
from plannings.models import Planning

class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = ['id', 'name', 'activities', 'pto']
