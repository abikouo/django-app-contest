from django.db import models
import json


class Planning(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.TextField(blank=True)
    activities = models.CharField(default="PTO", max_length=2000)
    pto = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def set_activities(self, x):
        self.activities = json.dumps(x)

    def get_activities(self):
        return json.loads(self.activities)