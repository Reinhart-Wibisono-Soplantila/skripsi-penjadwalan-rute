import json
import calendar
from django.shortcuts import render
from django.views.generic import View
from app_outlet.models import OutletModel
from app_schedules.models import ScheduleModel
from datetime import datetime, timedelta
from django.db.models.functions import TruncMonth
from django.db.models import Count

def index(request):
    
    # Mengambil tanggal dan jam hari ini
    today = datetime.today()
    
    # Mencari tanggal pada hari senin minggu ini
    monday_this_week = today - timedelta(days=today.weekday())
    print('monday_this_week: ', monday_this_week)
    # MEncari tanggal pada hari senin dan sabtu minggu sebelumnya
    monday_last_week = monday_this_week - timedelta(weeks=1)
    sunday_last_week = monday_last_week + timedelta(days=6)
    print('monday_last_week:', monday_last_week)
    # first_day_last_month = today.replace(day=1) - timedelta(days=1)
    # first_day_last_month = first_day_last_month.replace(day=1)
    
    # Ambil data pengiriman dan jumlah toko untuk tiap rentang waktu
    # minggu ini
    shipments_this_week = ScheduleModel.objects.filter(Created_at__gte=monday_this_week).values('Schedule_id', 'Created_at')
    shipments_last_week = ScheduleModel.objects.filter(Created_at__gte=monday_last_week, Created_at__lt=sunday_last_week).values('Schedule_id', 'Created_at')
    shipments_this_year = ScheduleModel.objects.filter(Created_at__year=today.year).annotate(month=TruncMonth('Created_at')).values('month', 'Schedule_id')
    
    # List nama hari dari Senin hingga Sabtu
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
   
    
    # Membuat dictionary dengan key berupa nama hari
    schedule_by_day_this_week = {day: {'Count': 0} for day in day_names}
    schedule_by_day_last_week = {day: {'Count': 0} for day in day_names}
    schedule_by_year = {calendar.month_name[i]: {'Count': 0} for i in range(1, 13)}
    day_before=''
    # Isi dictionary dengan data yang ditemukan
    for current_shipment in shipments_this_week:
        day_name = current_shipment['Created_at'].strftime('%A')
        if day_name in schedule_by_day_this_week:
            if day_before==day_name:
                outlet_count += ScheduleModel.objects.get(Schedule_id=current_shipment['Schedule_id']).Total_location
                # Simpan informasi dalam dictionary per hari
                schedule_by_day_this_week[day_name] = {
                    'Count': outlet_count
                } 
            else:
                outlet_count = ScheduleModel.objects.get(Schedule_id=current_shipment['Schedule_id']).Total_location
                # Simpan informasi dalam dictionary per hari
                schedule_by_day_this_week[day_name] = {
                    'Count': outlet_count
                }
            day_before = day_name
            
    for last_shipment in shipments_last_week:
        day_name = last_shipment['Created_at'].strftime('%A')
        if day_name in schedule_by_day_last_week:
            if day_before==day_name:
                outlet_count += ScheduleModel.objects.get(Schedule_id=last_shipment['Schedule_id']).Total_location
                # Simpan informasi dalam dictionary per hari
                schedule_by_day_last_week[day_name] = {
                    'Count': outlet_count
                } 
            else:
                outlet_count = ScheduleModel.objects.get(Schedule_id=last_shipment['Schedule_id']).Total_location
                # Simpan informasi dalam dictionary per hari
                schedule_by_day_last_week[day_name] = {
                    'Count': outlet_count
                }
            day_before = day_name
    for year_shipment in shipments_this_year:
        # Ambil Schedule_id
        schedule_id = year_shipment['Schedule_id']
        
        # Ambil jumlah outlet yang dituju pada setiap Schedule_id
        outlets_count = ScheduleModel.objects.get(Schedule_id=schedule_id).Total_location
        
        # Ambil nama bulan dari field 'month'
        month_name = year_shipment['month'].strftime('%B')
        
        # Tambahkan jumlah outlet ke dictionary yang sesuai
        schedule_by_year[month_name]['Count'] += outlets_count
        
    print('months_of_year: ', schedule_by_year)     
    for day, scheduleData in schedule_by_day_this_week.items():
        print(f"{day}: {scheduleData}") 
    for day, scheduleData in schedule_by_day_last_week.items():
        print(f"{day}: {scheduleData}")
        
    context = {
        'schedule_by_day_this_week_json': json.dumps(schedule_by_day_this_week),
        'schedule_by_day_this_last_json': json.dumps(schedule_by_day_last_week),
        'schedule_by_year_json': json.dumps(schedule_by_year),
    }
    return render(request, 'dashboard/index.html', context)

