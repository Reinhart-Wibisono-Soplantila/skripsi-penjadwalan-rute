import os
import json
import pytz
import folium
import polyline
import pandas as pd
from .forms import StatusForm
from app_schedules.algorithm.GA import GeneticAlgorithm 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.staticfiles import finders
from django.contrib import messages
from django.db.models import Case, When
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from app_schedules.models import ScheduleModel, ScheduleOutlet, ScheduleVehicle
from app_vehicle.models import VehicleModel
from app_outlet.models import OutletModel
from app_report.models import Map
from django.db.models import Q
from django.utils import timezone
from django.utils.timezone import make_naive
from proweb.decorators import group_required
# Create your views here.
@group_required('Admin', 'Driver')
def index(request):
    ScheduleObject = ScheduleModel.objects.all()
    # Konversi waktu UTC ke zona waktu lokal pengguna
    display_timezone = pytz.timezone('Asia/Makassar')
    for item in ScheduleObject:
        print(f"UTC Time: {item.Created_at}, Local Time: {item.Created_at.astimezone(display_timezone)}")
        
        # item.Created_at = item.Created_at.astimezone(display_timezone)
        item.Created_at = make_naive(item.Created_at, display_timezone)
        print(item.Created_at)
    print('')
    for item in ScheduleObject:
        print(item.Created_at)
    context = {
        'ScheduleObject' : ScheduleObject,
    }
    print(context)
    return render(request, 'report/index.html', context)

@group_required('Admin', 'Driver')
def maps(request, Schedule_id, Vehicle_id):
    
    existing_map = Map.objects.filter(name=f'{Schedule_id}-{Vehicle_id}').first()
    if existing_map:
        # Jika sudah ada, kembalikan file path atau response sesuai kebutuhan
        return render(request, f'maps/{Schedule_id}-{Vehicle_id}.html')
    else:
        ScheduleObject = ScheduleOutlet.objects.filter( Q(Group_vehicle_number=Vehicle_id) & Q(Schedule_id=Schedule_id)).order_by('id')
        AllRoute=[]
        for iteration in range(len(ScheduleObject)-1):
            firstKey = ScheduleObject.values_list('OutletCode', flat=True)[iteration]
            secondKey = ScheduleObject.values_list('OutletCode', flat=True)[iteration+1]
            AllRoute.append(f'{firstKey}, {secondKey}')
        # print(Route)
        
        json_file_path = finders.find('files/distanceMatrix.json')
        data = {}
        if json_file_path:
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                
        start_route = AllRoute[0]
        start_location = [data[start_route]['from']['outlet_coord'][1], data[start_route]['from']['outlet_coord'][0]]
        result_map = folium.Map(location=start_location, zoom_start=12)

        # Loop hanya melalui rute yang dipilih
        
        i=0
        for key in AllRoute:
            if key in data:
                location_to = OutletModel.objects.filter(OutletCode=data[key]['to']['outlet_code']).values_list('OutletName', flat=True).first()
                location_from = OutletModel.objects.filter(OutletCode=data[key]['from']['outlet_code']).values_list('OutletName', flat=True).first()
                
                route_data = data[key]
                from_coord = route_data['from']['outlet_coord']
                from_coord = [from_coord[1], from_coord[0]]
                
                to_coord = route_data['to']['outlet_coord']
                to_coord = [to_coord[1], to_coord[0]]
                
                if i == 0:
                    folium.Marker(
                        location = from_coord,
                        popup=folium.Popup( f"""Start : {location_from}""",max_width=500),
                    ).add_to(result_map)
                    
                folium.Marker(
                    location = from_coord,
                    popup=folium.Popup( f"""From: {location_from} - To: {location_to}""",max_width=500),
                    icon=folium.DivIcon(html=f"""<div style="font-size: 20pt; font-weight: bold; color: black">{i}</div>""")
                ).add_to(result_map)
                
                folium.Marker(
                    location = to_coord,
                    popup=folium.Popup( f"""From: {location_from} - To: {location_to}""",max_width=500),
                ).add_to(result_map)
                
                if i==len(AllRoute)-1:
                    folium.Marker(
                        location = to_coord,
                        icon=folium.DivIcon(html=f"""<div style="font-size: 20pt; font-weight: bold; color: black">{i+1}</div>""")
                    ).add_to(result_map)
                    
                # Decode geometri polyline dan tambahkan ke peta sebagai PolyLine
                encoded_geometri = route_data['geometri']
                decoded_coords = polyline.decode(encoded_geometri)
                
                # Tambahkan rute ke peta
                folium.PolyLine(decoded_coords, color="blue", weight=2.5, opacity=1).add_to(result_map)
            i+=1
            
            file_path = os.path.join('app_report', 'templates', 'maps', f'{Schedule_id}-{Vehicle_id}.html')
            
        # Simpan peta ke file HTML
        result_map.save(file_path)
        Map.objects.create(name=f'{Schedule_id}-{Vehicle_id}', Schedule_id=Schedule_id, file_path=file_path)
        return render(request, f'maps/{Schedule_id}-{Vehicle_id}.html')
        # return redirect(reverse('app_report:view', kwargs={'Schedule_id':Schedule_id}))

@group_required('Admin', 'Driver')
def view(request, Schedule_id):
    # Retrieve data for view page section
    VehicleSchedule = ScheduleVehicle.objects.filter(Schedule_id=Schedule_id)
    
    json_file_path = finders.find('files/distanceMatrix.json')
    data = {}
    if json_file_path:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            
    RouteListed={}
    for vehicle in VehicleSchedule:
        key = vehicle.VehicleNumber_id
        ScheduleObject = ScheduleOutlet.objects.filter(
            Q(Group_vehicle_number=key) & Q(Schedule_id=Schedule_id)).order_by('id')
        vehicleObject = VehicleModel.objects.get(VehicleNumber=key)
        RouteListed[key] = {
            'NumberLocation':vehicle.Total_location_each_vehicle, 
            'detailsVehicle':{
                'ScheduleId' : Schedule_id,
                'VehicleNumber' : vehicleObject.VehicleNumber,
                'VehicleType' : vehicleObject.UnitType,
                'DriverName' : vehicleObject.DriverName,
                'TotalDistance' : vehicle.Total_distance_each_vehicle,
                'TotalOutlets' : vehicle.Total_location_each_vehicle
            }
        }
        if 'detailsRoute' not in RouteListed[key]:
            RouteListed[key]['detailsRoute'] = {}
        for iteration in range(len(ScheduleObject)-1):
            firstKey = ScheduleObject.values_list('OutletCode', flat=True)[iteration]
            secondKey = ScheduleObject.values_list('OutletCode', flat=True)[iteration+1]
            statusRoute = ScheduleObject.values_list('Status', flat=True)[iteration+1]
            
            firstOutlet = OutletModel.objects.get(OutletCode=firstKey).OutletName
            secondOutlet = OutletModel.objects.get(OutletCode=secondKey).OutletName
            
            firstOutlet_Address = OutletModel.objects.get(OutletCode=firstKey).Address
            secondOutlet_Address = OutletModel.objects.get(OutletCode=secondKey).Address
            
            searchedKey = f'{firstKey}, {secondKey}'
            FilteredDict = {key: value for key, value in data.items() if key == searchedKey}
            distance = FilteredDict.get(searchedKey, {})
            distance = distance.get('jarak')
            RouteListed[key]['detailsRoute'][searchedKey]={
                'firstOutlet' : firstOutlet,
                'secondOutlet' : secondOutlet,
                'secondCode' : secondKey,
                'from_address' : firstOutlet_Address,
                'to_address' : secondOutlet_Address,
                'distance' : distance,
                'status' : statusRoute
            }
            
    # Change Status Section
    statusForm = StatusForm(request.POST or None)
    error = None
    if request.method == 'POST':
        if statusForm.is_valid():
            selected_outlets_data = request.POST.get("selected-outlets")
            # Parse JSON string menjadi list of dictionaries
            print(selected_outlets_data)
            status = statusForm.cleaned_data['Status']
            try:
                selected_outlets = json.loads(selected_outlets_data)
            except json.JSONDecodeError:
                print('error')
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            if not selected_outlets_data:
                print('Error: No outlets selected')
                messages.error(request, "You must select at least one outlet.")
                return redirect('your_view_name')
            # Loop untuk memproses setiap outlet yang dipilih
            for outlet_data in selected_outlets:
                vehicle_id = outlet_data.get("vehicleId")
                schedule_id = outlet_data.get("scheduleId")
                selected_outlet_ids = outlet_data.get("selectedOutlets", [])

                # Proses untuk mengupdate status berdasarkan vehicle_id, schedule_id, dan outlet yang dipilih
                # Misalnya, Anda mencari record di database dan mengubah statusnya
                # Pastikan model dan field sesuai dengan data yang Anda miliki
                ScheduleOutlet.objects.filter(
                    Group_vehicle_number=vehicle_id,
                    Schedule_id=schedule_id,
                    OutletCode_id__in=selected_outlet_ids
                ).update(Status=status)
                return redirect(reverse('app_report:view', kwargs={'Schedule_id':Schedule_id}))
        else:
            error = statusForm.errors
            
    context = {
        'RouteListed' : RouteListed,
        'Schedule_id' : Schedule_id,
        'form': statusForm,
        'error':error,
    }
    
    # print(RouteListed)
    return render(request, 'report/view.html', context)

@group_required('Admin')
def add(request, Schedule_id, Vehicle_id):
    # Retrieve data for add outlet section
    OutletObject = OutletModel.objects.exclude(OutletType='Source')
    
    request.session.pop('outlets', None)
    request.session.pop('vehicle_id', None)
    request.session.pop('schedule_id', None)
    request.session.pop('ScheduleResult', None)
    
    error={}
    if request.method == 'POST':
        CheckedList = request.POST.get('selected_outlets', '')
        
        if not CheckedList:
            error['selected_outlets'] = "You must select at least one option."
            messages.error(request, error['selected_outlets'])
        if not error:
            outlets = [str(x) for x in CheckedList.split(',')]
            request.session['outlets'] = outlets
            request.session['vehicle_id'] = Vehicle_id
            request.session['schedule_id'] = Schedule_id
            return redirect('app_report:processoutlets')
            
    context={
        'Schedule_id' : Schedule_id,
        'Vehicle_id' : Vehicle_id,
        'OutletObject' : OutletObject
    }
    return render(request, 'report/add.html', context)

@group_required('Admin')
def processoutlets(request):
    outlets = request.session.get('outlets', [])
    # Find best route from all outlets
    # GA
    GA = GeneticAlgorithm()
    result, genNumber  = GA.main(outlets)
    print( result)
    DeliveryList={}
    result[1].insert(0, '15000000000000000000000000')
    DeliveryList = {'distance':result[0], 'outlets':result[1]}
    
    print('DeliveryList')
    print(DeliveryList)
    request.session['ScheduleResult'] = DeliveryList
    
    # # SMO
    # SMO = SpiderMonkeyAlgorithm()
    # location, fitness = SMO.main(outlets)
    # print(location)
    # print('')
    # print(fitness)
            
    # Hapus data dari sesi jika tidak diperlukan lagi
    # request.session.pop('cities_ids', None)
    return redirect('app_report:result')
    # return redirect('app_schedules:vehicles')

@group_required('Admin')
def result(request):
    schedule = request.session.get('ScheduleResult', [])
    vehicle_id = request.session.get('vehicle_id', [])
    schedule_id = request.session.get('schedule_id', [])
    json_file_path = finders.find('files/distanceMatrix.json')
    data = {}
    
    if json_file_path:
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
    
    OutletObject = OutletModel.objects.filter(OutletCode__in=schedule['outlets']).order_by(
        Case(*[When(OutletCode=id, then=pos) for pos, id in enumerate(schedule['outlets'])])
        )
    
    VehicleObject = VehicleModel.objects.get(VehicleNumber = vehicle_id)
    schedule['detailsRoute'] = {}
    for iteration in range(len(OutletObject)-1):
            firstKey = OutletObject.values_list('OutletCode', flat=True)[iteration]
            secondKey = OutletObject.values_list('OutletCode', flat=True)[iteration+1]
            searchedKey = f'{firstKey}, {secondKey}'
            FilteredDict = {key: value for key, value in data.items() if key == searchedKey}
            distance = FilteredDict.get(searchedKey, {})
            distance = distance.get('jarak')
            firstOutlet = OutletModel.objects.get(OutletCode=firstKey).OutletName
            secondOutlet = OutletModel.objects.get(OutletCode=secondKey).OutletName
            schedule['detailsRoute'][searchedKey] = {
                    'firstOutlet' : firstOutlet,
                    'secondOutlet' : secondOutlet,
                    'distance' : distance
                }
            schedule['detailsVehicle']={
                'VehicleNumber' : VehicleObject.VehicleNumber,
                'VehicleType' : VehicleObject.UnitType,
                'DriverName' : VehicleObject.DriverName,
            }
            schedule['TotalOutlets'] = len(schedule['outlets'])-1
    context ={
        'schedule' : schedule,
        'Schedule_id' : schedule_id,
        'Vehicle_id' : vehicle_id
    }
    
    print('schedule')
    print(schedule)
    return render(request, 'report/result.html', context)
    # VehicleSchedule = ScheduleVehicle.objects.filter(Q(Group_vehicle_number=Vehicle_id) & Q(Schedule_id=Schedule_id))
    # RouteListed={}
    # ScheduleObject = ScheduleOutlet.objects.filter(
    #     Q(Group_vehicle_number=Vehicle_id) & Q(Schedule_id=Schedule_id)).order_by('id')
    # vehicleObject = VehicleModel.objects.get(VehicleNumber=Vehicle_id)
    # RouteListed = {
    #     'NumberLocation':VehicleSchedule.Total_location_each_vehicle, 
    #     'detailsVehicle':{
    #         'ScheduleId' : Schedule_id,
    #         'VehicleNumber' : vehicleObject.VehicleNumber,
    #         'VehicleType' : vehicleObject.UnitType,
    #         'DriverName' : vehicleObject.DriverName,
    #         'TotalDistance' : VehicleSchedule.Total_distance_each_vehicle,
    #         'TotalOutlets' : VehicleSchedule.Total_location_each_vehicle
    #     }
    # }
    # RouteListed['detailsRoute'] = {}
    # for iteration in range(len(ScheduleObject)-1):
    #     firstKey = ScheduleObject.values_list('OutletCode', flat=True)[iteration]
    #     secondKey = ScheduleObject.values_list('OutletCode', flat=True)[iteration+1]
    #     statusRoute = ScheduleObject.values_list('Status', flat=True)[iteration+1]
        
    #     firstOutlet = OutletModel.objects.get(OutletCode=firstKey).OutletName
    #     secondOutlet = OutletModel.objects.get(OutletCode=secondKey).OutletName
        
    #     searchedKey = f'{firstKey}, {secondKey}'
    #     FilteredDict = {key: value for key, value in data.items() if key == searchedKey}
    #     distance = FilteredDict.get(searchedKey, {})
    #     distance = distance.get('jarak')
    #     RouteListed['detailsRoute'][searchedKey]={
    #         'firstOutlet' : firstOutlet,
    #         'secondOutlet' : secondOutlet,
    #         'secondCode' : secondKey,
    #         'distance' : distance,
    #         'status' : statusRoute
    #     }
        
@group_required('Admin')
def delete(request, Schedule_id):
    ScheduleObject = ScheduleModel.objects.get(pk=Schedule_id)
    ScheduleObject.delete()
    return redirect('app_report:index')