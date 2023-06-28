from rest_framework import serializers
from schedule.models import Plannings


class PlanningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plannings
        fields = ['id', 'name', 'activities', 'pto']
