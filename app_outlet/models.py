from django.db import models
from django.utils import timezone

# Create your models here.

    
class OutletModel(models.Model):
    OutletCode=models.CharField(
        max_length=255,
        primary_key=True
    )
    OutletNumber=models.CharField(
        max_length=255
    )
    OutletName=models.CharField(
        max_length=255
    )
    OutletType=models.CharField(
        max_length=255,
        null=True
    )
    Address=models.CharField(
        max_length=255
    )
    Provinsi=models.CharField(
        max_length=255
    )
    Kabupaten=models.CharField(
        max_length=255
    )
    Kecamatan=models.CharField(
        max_length=255
    )
    Kelurahan=models.CharField(
        max_length=255
    )
    Latitude=models.CharField(
        max_length=255
    )
    Longitude=models.CharField(
        max_length=255
    )
    Days=models.CharField(
        max_length=255
    )
    Delivery=models.CharField(
        max_length=255
    )
    Created_at=models.DateTimeField(
        auto_now_add=True
    )
    Updated_at=models.DateTimeField(
        auto_now=True
    )

# class reg_Provinces(models.Model):
#     name=models.CharField(
#         max_length=255
#     )
#     def __str__(self):
#         return self.name
    
# class reg_Regencies(models.Model):
#     province=models.ForeignKey(reg_Provinces, on_delete=models.CASCADE)
#     name=models.CharField(
#         max_length=255
#     )
#     def __str__(self):
#         return self.name

# class reg_Districts(models.Model):
#     regency=models.ForeignKey(reg_Regencies, on_delete=models.CASCADE)
#     name=models.CharField(
#         max_length=255
#     )
#     def __str__(self):
#         return self.name
    
# class reg_Villages(models.Model):
#     district=models.ForeignKey(reg_Districts, on_delete=models.CASCADE)
#     name=models.CharField(
#         max_length=255
#     )
#     def __str__(self):
#         return self.name