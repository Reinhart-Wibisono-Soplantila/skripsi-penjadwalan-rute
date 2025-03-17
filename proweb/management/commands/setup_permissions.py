# Di dalam file management/commands/setup_permissions.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app_schedules.models import ScheduleModel
from app_outlet.models import OutletModel
from app_vehicle.models import VehicleModel

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create groups
        admin_group, created = Group.objects.get_or_create(name='Admin')
        driver_group, created = Group.objects.get_or_create(name='Driver')

        # Assign permissions to Admin group
        if created:
            permissions = Permission.objects.all()
            admin_group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS('Admin group created and permissions assigned.'))

        # Assign specific permissions to Driver group
        # Get ContentType for ScheduleModel and OutletModel
        schedule_content_type = ContentType.objects.get_for_model(ScheduleModel)
        outlet_content_type = ContentType.objects.get_for_model(OutletModel)
        # driver_content_type = ContentType.objects.get_for_model(DriverModel)
        vehicle_content_type = ContentType.objects.get_for_model(VehicleModel)
        
        # Get permissions for those models
        schedule_permissions = Permission.objects.filter(content_type=schedule_content_type, codename='view_schedulemodel')
        outlet_permissions = Permission.objects.filter(content_type=outlet_content_type, codename='view_outletmodel')
        # driver_permissions = Permission.objects.filter(content_type=driver_content_type, codename='view_drivermodel')
        vehicle_permissions = Permission.objects.filter(content_type=vehicle_content_type, codename='view_vehiclemodel')  

        # Combine permissions
        driver_account_permissions = schedule_permissions | outlet_permissions | vehicle_permissions

        driver_group.permissions.set(driver_account_permissions)
        self.stdout.write(self.style.SUCCESS('Driver group created and permissions assigned for ScheduleModel and OutletModel.'))