from django.urls import path
from . import views

app_name='app_vehicle'
urlpatterns = [
        
    path('', views.vehicle_index, name='vehicleIndex'),
    path('create', views.vehicle_create, name='vehicleCreate'),
    path('update/<str:vehicleNumber>', views.vehicle_update, name='vehicleUpdate'),
    path('delete/<str:vehicleNumber>', views.vehicle_delete, name='vehicleDelete'),
    
    # path('driver/create', views.driver_create, name='driverCreate'),
    # path('driver/update/<str:driverId>', views.driver_update, name='driverUpdate'),
    # path('driver/view/<str:driverId>', views.driver_view, name='driverView'),
    # path('driver/delete/<str:driverId>', views.driver_delete, name='driverDelete'),
]
