import json
import numpy as np
from django.shortcuts import render, redirect
from django.db.models import Case, When
from django.contrib.staticfiles import finders
from django.contrib import messages
from app_outlet.models import OutletModel
from app_schedules.models import ScheduleModel, ScheduleVehicle, ScheduleOutlet
from app_vehicle.models import VehicleModel
from .algorithm.GA import GeneticAlgorithm 
from .algorithm.SMO import SpiderMonkeyAlgorithm
from django.utils import timezone
from datetime import datetime
from proweb.decorators import group_required
from django.templatetags.static import static
from django.http import JsonResponse

@group_required('Admin')
def index(request):
    # OutletObject = OutletModel.objects.all()
    OutletObject = OutletModel.objects.exclude(OutletType='Source')
    error={}
    
    request.session.pop('ScheduleResult', None)
    request.session.pop('vehicles', None)
    request.session.pop('outlets', None)
    if request.method == 'POST':
        CheckedList = request.POST.get('selected_outlets', '')
        
        if not CheckedList:
            error['selected_outlets'] = "You must select at least one option."
            messages.error(request, error['selected_outlets'])
        if not error:
            outlets = [str(x) for x in CheckedList.split(',')]
            request.session['outlets'] = outlets
            return redirect('app_schedules:viewoutlets')
        
    context={
        'error' : error,
        'OutletObject' : OutletObject
    }
    return render(request, 'schedule/index.html', context)

@group_required('Admin')
def viewoutlets(request):
    # Ambil ID dari sesi
    citiesId = request.session.get('outlets', [])
    OutletObject = OutletModel.objects.filter(OutletCode__in=citiesId)
    context={
        'OutletObject' : OutletObject
    }
    print(OutletObject)
    return render(request, 'schedule/confirm.html', context)

@group_required('Admin')
def vehicle(request):
    # VehicleObject = VehicleModel.objects.all()
    VehicleObject = VehicleModel.objects.filter(Status='Ready')
    error = {}
    if request.method == 'POST':
        vehicleList = request.POST.get('selected-vehicles', '')
        selectedAlgoritm = request.POST.get('algorithm', '')
        if not vehicleList:
            error['selected-vehicles'] = "You must select at least one vehicle."
            messages.error(request, error['selected-vehicles'])
        # if not selectedAlgoritm:
        #     error['algorithm'] = "You must select one algorithm before generate schedule."
        #     messages.error(request, error['algorithm'])
        if not error:
            vehicleList = json.loads(vehicleList)
            request.session['algorithm'] = selectedAlgoritm
            # vehicleList = vehicleList.split(',')
            request.session['vehicles'] = vehicleList
            print('check: ',vehicleList)
            print('check: ',selectedAlgoritm)
            # return JsonResponse({'GET': request.POST.dict()})
            return redirect('app_schedules:processoutlets')
    context={
        'VehicleObject' : VehicleObject,
    }
    return render(request, 'schedule/vehicle.html', context)

@group_required('Admin')
def processoutlets(request):
    outlets = request.session.get('outlets', [])
    vehicles = request.session.get('vehicles', [])
    algorithm = request.session.get('algorithm', [])
    vehicle_length = len(vehicles)
    outlets_length = len(outlets)
    
    if(algorithm == 'GA'):
        # Find best route from all outlets
        # GA
        GA = GeneticAlgorithm()
        result, genNumber  = GA.main(outlets)
        print( result)
        DeliveryList={}
        if vehicle_length > 1:
            divided_outlets_numpy = np.array_split(outlets, vehicle_length)
            divided_outlets = [sub_array.tolist() for sub_array in divided_outlets_numpy]
            group=0
            while group<vehicle_length:
                # GA
                GA = GeneticAlgorithm()
                result, genNumber  = GA.main(divided_outlets[group])
                result[1].insert(0, '15000000000000000000000000')
            
                print('answer=', result[0])
                print('location=', result[1])
                DeliveryList[vehicles[group]] = {'distance':result[0], 'outlets':result[1]}
                group+=1
        else:
            result[1].insert(0, '15000000000000000000000000')
            DeliveryList[vehicles[0]] = {'distance':result[0], 'outlets':result[1]}
    
        print(DeliveryList)
        request.session['ScheduleResult'] = DeliveryList
    elif(algorithm == 'SMO'):
        # SMO
        SMO = SpiderMonkeyAlgorithm()
        location, fitness = SMO.main(outlets)
        
        DeliveryList={}
        if vehicle_length > 1:
            divided_outlets_numpy = np.array_split(outlets, vehicle_length)
            divided_outlets = [sub_array.tolist() for sub_array in divided_outlets_numpy]
            group=0
            while group<vehicle_length:
                # SMO
                SMO = SpiderMonkeyAlgorithm()
                location, fitness = SMO.main(divided_outlets[group])
                
                location.insert(0, '15000000000000000000000000')
                print('answer=', fitness)
                print('location=', location)
                DeliveryList[vehicles[group]] = {'distance':fitness, 'outlets':location}
                group+=1
        else:
            location.insert(0, '15000000000000000000000000')
            DeliveryList[vehicles[0]] = {'distance':fitness, 'outlets':location}
    
        print(DeliveryList)
        request.session['ScheduleResult'] = DeliveryList
    return redirect('app_schedules:result')

@group_required('Admin')
def result(request):
    schedule = request.session.get('ScheduleResult', [])
    print()
    print(schedule)
    print()
    vehicles = request.session.get('vehicles', [])
    # Find the path to the JSON file
    json_file_path = finders.find('files/distanceMatrix.json')
    data = {}
    if json_file_path:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    for key, subkey in schedule.items():
        OutletObject = OutletModel.objects.filter(OutletCode__in=schedule[key]['outlets']).order_by(
            Case(*[When(OutletCode=id, then=pos) for pos, id in enumerate(schedule[key]['outlets'])])
            )
        if 'detailsRoute' not in subkey:
            subkey['detailsRoute'] = {}
        print(key)
        VehicleObject = VehicleModel.objects.get(VehicleNumber = key)
        print(VehicleObject)
        for iteration in range(len(OutletObject)-1):
            firstKey = OutletObject.values_list('OutletCode', flat=True)[iteration]
            secondKey = OutletObject.values_list('OutletCode', flat=True)[iteration+1]
            searchedKey = f'{firstKey}, {secondKey}'
            FilteredDict = {key: value for key, value in data.items() if key == searchedKey}
            distance = FilteredDict.get(searchedKey, {})
            distance = distance.get('jarak')
            firstOutlet = OutletModel.objects.get(OutletCode=firstKey).OutletName
            secondOutlet = OutletModel.objects.get(OutletCode=secondKey).OutletName
            
            firstOutlet_Address = OutletModel.objects.get(OutletCode=firstKey).Address
            secondOutlet_Address = OutletModel.objects.get(OutletCode=secondKey).Address
            
            subkey['detailsRoute'][searchedKey] = {
                    'from_Outlet' : firstOutlet,
                    'to_Outlet' : secondOutlet,
                    'distance' : distance,
                    'from_address' : firstOutlet_Address,
                    'to_address' : secondOutlet_Address,
                }
            subkey['detailsVehicle']={
                'VehicleNumber' : VehicleObject.VehicleNumber,
                'VehicleType' : VehicleObject.UnitType,
                'DriverName' : VehicleObject.DriverName,
            }
            subkey['TotalOutlets'] = len(schedule[key]['outlets'])-1
        print(f'sudah{key}')
    if request.method == 'POST':
        scheduleModel = ScheduleModel()
        scheduleModel.Total_location = len(request.session.get('outlets', []))
        scheduleModel.save()
        
        for key in schedule:
            for outlet in schedule[key]['outlets']:
                print(f"{key}, {outlet}")
                ScheduleOutlet.objects.create(
                    OutletCode_id = outlet,
                    Group_vehicle_number = key,
                    Schedule = scheduleModel
                )
            ScheduleVehicle.objects.create(
                VehicleNumber_id = schedule[key]['detailsVehicle']['VehicleNumber'],
                Total_location_each_vehicle = schedule[key]['TotalOutlets'],
                Schedule = scheduleModel,
                Total_distance_each_vehicle=schedule[key]['distance']
            )
            
        VehicleObject = VehicleModel.objects.filter(VehicleNumber__in=vehicles)
        for vehicle in VehicleObject:
            vehicle.Status = 'Used'
            vehicle.Used_at = timezone.now()
            vehicle.save()
            
            request.session.pop('ScheduleResult', None)
            request.session.pop('vehicles', None)
            request.session.pop('outlets', None)
            return redirect('app_report:index')
        
    context ={
        'schedule' : schedule
    }
    return render(request, 'schedule/result.html', context)
    # return render(request, 'schedule/result.html')