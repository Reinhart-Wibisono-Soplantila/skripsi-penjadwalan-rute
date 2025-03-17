from django.db import models

# Create your models here.
class VehicleModel(models.Model):
    UnitType=models.CharField(
        max_length=255
    )
    VehicleNumber=models.CharField(
        max_length=20,
        primary_key=True
    )
    DriverName=models.CharField(
        max_length=255
    )
    Status=models.CharField(
        max_length=20,
        default='Ready'
    )
    Created_at=models.DateTimeField(
        auto_now_add=True
    )
    Updated_at=models.DateTimeField(
        auto_now=True
    )
    Used_at=models.DateTimeField(
        blank=True,
        null=True
    )
    
    def __str__(self):
        return"{}. {}".format(self.VehicleNumber, self.DriverName)
    
# class DriverModel(models.Model):
#     FullName=models.CharField(
#         max_length=255
#     )
#     Phone=models.CharField(
#         max_length=30
#     )
#     Address=models.TextField()
#     Created_at=models.DateTimeField(
#         auto_now_add=True
#     )
#     Updated_at=models.DateTimeField(
#         auto_now=True
#     )
#     Used_at=models.DateTimeField(
#         blank=True,
#         null=True
#     )
    
#     def __str__(self):
#         return"{}. {}".format(self.id, self.FullName)