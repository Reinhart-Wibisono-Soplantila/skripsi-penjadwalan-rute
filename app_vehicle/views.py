from django.shortcuts import render, redirect, get_object_or_404
from .models import VehicleModel
from .form import VehicleForm
from proweb.decorators import group_required
# Create your views here.

# vehicle views
@group_required('Admin', 'Driver')
def vehicle_index(request):
    VehicleObject = VehicleModel.objects.all()
    context={
        'PageHeader' : 'Vehicle & Driver',
        'VehicleLink': 'app_vehicle:vehicleCreate', 
        'VehicleButton' : 'Add Vehicle',
        'DriverLink' : 'app_vehicle:driverCreate',
        'DriverButton' : 'Add Driver',
        'VehicleDatas' : VehicleObject,
    }
    return render(request, 'vehicle/index.html', context)

@group_required('Admin')
def vehicle_create(request):
    VehicleForm_Create = VehicleForm(request.POST or None)
    error = None
    if request.method == 'POST':
        if VehicleForm_Create.is_valid():
            VehicleForm_Create.save()
            return redirect('app_vehicle:vehicleIndex')
        else:
            error = VehicleForm_Create.errors
    context={
        'pageHeader' : 'Add Vehicle',
        'form': VehicleForm_Create,
        'error' : error 
    }
    return render(request, 'vehicle/create.html', context)

@group_required('Admin')
def vehicle_update(request, vehicleNumber):
    updated_data = get_object_or_404(VehicleModel, VehicleNumber=vehicleNumber)
    VehicleForm_updated = VehicleForm(request.POST or None, instance=updated_data)
    error = None
    if(request.method == 'POST'):
        if(VehicleForm_updated.is_valid()):
            VehicleForm_updated.save()
            return redirect('app_vehicle:vehicleIndex')
        else:
            error = VehicleForm_updated.errors
    context={
        'pageHeader' : 'Vehicle Update',
        'form':VehicleForm_updated,
        'error':error
    }
    return render(request, 'vehicle/update.html', context)

@group_required('Admin')
def vehicle_delete(request, vehicleNumber):
    VehicleModel.objects.filter(VehicleNumber = vehicleNumber).delete()
    return redirect('app_vehicle:vehicleIndex')

# driver views
# @group_required('Admin')
# def driver_create(request):
#     DriverForm_Create = DriverForm(request.POST or None)
#     error = None
#     if request.method == 'POST':
#         if DriverForm_Create.is_valid():
#             DriverForm_Create.save()
#             return redirect('app_vehicle:vehicleIndex')
#         else:
#             # print(DriverForm_Create.errors)
#             error = DriverForm_Create.errors
#     context={
#         'pageHeader' : 'Add Driver',
#         'form' : DriverForm,
#         'error' : error
#     }
#     return render(request, 'driver/create.html', context)

# @group_required('Admin')
# def driver_update(request, driverId):
#     updated_data = get_object_or_404(DriverModel, id=driverId)
#     DriverForm_updated = DriverForm(request.POST or None, instance=updated_data)
#     error = None
#     if(request.method == 'POST'):
#         if(DriverForm_updated.is_valid()):
#             DriverForm_updated.save()
#             return redirect('app_vehicle:vehicleIndex')
#         else:
#             error = DriverForm_updated.errors
#     context={
#         'pageHeader' : 'Driver Update',
#         'form':DriverForm_updated,
#         'error':error
#     }
#     return render(request, 'driver/update.html', context)

# @group_required('Admin', 'Driver')
# def driver_view(request, driverId):
#     selected_data = get_object_or_404(DriverModel, id=driverId)
#     DriverForm_selected = DriverForm(instance=selected_data)
    
#     for field in DriverForm_selected.fields.values():
#         field.widget.attrs['disabled'] = 'disabled'
    
#     context = {
#         'pageHeader' : 'View Driver',
#         'form' : DriverForm_selected
#     }
#     return render(request, 'driver/view.html', context)

# @group_required('Admin')
# def driver_delete(request, driverId):
#     DriverModel.objects.filter(id=driverId).delete()
#     return redirect('app_vehicle:vehicleIndex')