from django.db import models
from django.utils import timezone
from app_outlet.models import OutletModel
from app_vehicle.models import VehicleModel
# Create your models here.

def generate_default_id():
    # Mendapatkan tanggal saat ini dalam format YYYYMMDD
    date_str = timezone.now().strftime("%Y-%m-%d")
    # Menentukan awalan huruf dan nomor urut
    prefix = ['A', 'B', 'C', 'D', 'E']
    max_number = 99  # Maksimal nomor urut sebelum huruf berubah
    
    # Mencari ID terakhir dengan tanggal yang sama
    last_id = ScheduleModel.objects.filter(Created_at__date=date_str).order_by('Schedule_id').last()
    
    if last_id:
        # Mengambil bagian huruf dan nomor urut
        id_parts = last_id.Schedule_id.split('-')
        
        # Huruf dari ID terakhir
        last_prefix = id_parts[3][0]  # Mengambil huruf dari ID terakhir
        print("last prefix", last_prefix)
        # Nomor urut dari ID terakhir
        last_number_str = id_parts[3][1:]  # Mengambil nomor urut dari ID terakhir
        print(last_number_str)
        last_number = int(last_number_str)
        print(last_number)
        
        # Menghitung nomor urut berikutnya dan huruf baru
        if last_number >= max_number:
            # Jika nomor urut melebihi batas, ubah huruf
            next_number = 1
            for index in range(len(prefix)):
                if prefix[index] == last_prefix:
                    print(f"{prefix[index]}=={last_prefix}")
                    next_prefix = prefix[index+1]
                    print(next_prefix)
                    break
            # next_prefix = chr(ord(last_prefix) + 1)  # Ubah huruf
        else:
            next_number = last_number + 1
            next_prefix = last_prefix
        
        # Format nomor urut dengan padding nol (2 digit)
        new_id = f"{date_str}-{next_prefix}{next_number:02}"
        print('newid = ', new_id)
    else:
        # ID pertama
        new_id = f"{date_str}-{prefix[0]}01"
    
    return new_id

class ScheduleModel(models.Model):
    Schedule_id=models.CharField(
        max_length=255,
        primary_key=True,
        default=generate_default_id,
    )
    Total_location = models.IntegerField()
    Destination_outlet = models.ManyToManyField(
        OutletModel, 
        through='ScheduleOutlet',
        related_name='outlets_sc'
    )
    Vehicle_used=models.ManyToManyField(
        VehicleModel, 
        through='ScheduleVehicle',
        related_name='vehicles_sc'
    )
    Created_at=models.DateTimeField(
        auto_now_add=True
    )
    Updated_at=models.DateTimeField(
        auto_now=True
    )

class ScheduleOutlet(models.Model):
    Schedule = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE)
    OutletCode = models.ForeignKey(OutletModel, on_delete=models.CASCADE)
    Group_vehicle_number = models.CharField(max_length=255)
    Status = models.CharField(max_length=20, default='On progress')  

class ScheduleVehicle(models.Model):
    Schedule = models.ForeignKey(ScheduleModel, on_delete=models.CASCADE)
    VehicleNumber = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    Total_location_each_vehicle = models.IntegerField()
    Total_distance_each_vehicle = models.FloatField(default=0.0)