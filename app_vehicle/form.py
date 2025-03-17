from django import forms
from .models import VehicleModel

class VehicleForm(forms.ModelForm):
    StatusChoices=(
        ("Ready", 'Ready'),
        ('Repaired', 'Repaired'),
        ('Used', 'Used'),
    )
    Status = forms.ChoiceField(
        choices=StatusChoices,
        required=False,
        widget=forms.Select(
            attrs={
                'class' :'form-select form-control'
            }
        )
    )
    class Meta:
        model=VehicleModel
        fields = [
            'UnitType',
            'VehicleNumber',
            'DriverName',
            'Status',
        ]
        
        labels = {
            'UnitType' : 'Tipe Kendaraan',
            'VehicleNumber' : 'Nomor Kendaraan',
            'DriverName' : 'Nama Pengemudi'
        }
        
        error_messages ={
            'UnitType' : {
                'max_length' : 'Tipe Kendaraan terlalu panjang'
            },
            'VehicleNumber' : {
                'max_length': 'Nomor Kendaraan terlalu panjang',
                'unique': "Nomor Kendaraan sudah digunakan",
            },
            'DriverName':{
                'max_length' : 'Nama terlalu panjang'
            }
        }
        
        widgets = {
            'UnitType': forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "Masukkan Tipe Kendaraan"
                }
            ),
            'VehicleNumber' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "Masukkan Nomor Plat Kendaraan"
                }
            ),
            'DriverName' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : "Masukkan Nama Pengemudi"
                }
            )
        }
        