from django import forms
from .models import OutletModel

class OutletForm(forms.ModelForm):
    DeliveryStatus=(
        ("Daily", 'Daily'),
        ('Weekly', 'Weekly')
    )
    
    Days=(
        ("Monday", 'Senin'),
        ("Tuesday", 'Selasa'),
        ('Wednesday', 'Rabu'),
        ("Thursday", 'Kamis'),
        ('Friday', 'Jumat'),
        ('Saturday', 'Sabtu')
    )
    
    Delivery = forms.ChoiceField(
        choices=DeliveryStatus,
        required=False,
        label='Jenis Pengiriman',
        widget=forms.Select(
            attrs={
                'class' :'form-select form-control'
            }
        )
    )
    
    Days = forms.ChoiceField(
        choices=Days,
        required=False,
        label='Hari Pengiriman',
        widget=forms.Select(
            attrs={
                'class' :'form-select form-control'
            }
        )
    )
    
    class Meta:
        model=OutletModel
        fields = [
            'OutletNumber',
            'OutletCode',
            'OutletName',
            'OutletType',
            'Address',
            'Provinsi',
            'Kabupaten',
            'Kecamatan',
            'Kelurahan',
            'Latitude',
            'Longitude',
            'Days',
            'Delivery',
        ]
        
        labels = {
            'OutletNumber' : 'Nomor Toko',
            'OutletCode' : 'Kode Toko',
            'OutletName' : 'Nama Toko',
            'OutletType' : 'Tipe Toko',
            'Address' : 'Alamat',
            'Provinsi' : 'Provnsi',
            'Kabupaten' : 'Kabupaten',
            'Kecamatan' : 'Kecamatan',
            'Kelurahan' : 'Kelurahan',
            'Latitude' : 'Koordinat Latitude',
            'Longitude' : 'Koodinat Longitude',
        }
        
        widgets = {
            'OutletNumber' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Nomor Toko"
                }
            ),
            'OutletCode' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Kode Toko"
                }
            ),
            'OutletName' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Nama Toko"
                }
            ),
            'OutletType' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Tipe Toko"
                }
            ),
            'Address' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Alamat"
                }
            ),
            'Provinsi' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Provinsi"
                }
            ),
            'Kabupaten' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Kabupaten"
                }
            ),
            'Kecamatan' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Kecamatan"
                }
            ),
            'Kelurahan' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Kelurahan"
                }
            ),
            'Latitude' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Koordinat Latitude"
                }
            ),
            'Longitude' : forms.TextInput(
                attrs = {
                    'class' : 'form-control',
                    'placeholder' : "*Masukkan Koordinat Longitude"
                }
            ),
        }