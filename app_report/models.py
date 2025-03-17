from django.db import models
from app_schedules.models import ScheduleModel

# Create your models here.

class Map(models.Model):
    name = models.CharField(max_length=255)
    Schedule = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE, related_name='maps', default='Schedule_id')
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)