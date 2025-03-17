from django.utils import timezone

def active_menu(request):
    namespace = request.resolver_match.namespace
    url_name = request.resolver_match.url_name
    return {
        # 'current_url': f'{namespace}:{url_name}' if namespace else url_name
        'current_namespace' : f'{namespace}' if namespace else url_name
    }

def current_day_and_date(request):
    now = timezone.now()
    day_name = now.strftime("%A")
    current_date = now.strftime("%d %B %Y")
    
    return {
        'day_name': day_name,
        'current_date': current_date,
    }
    
def breadcrumb_context(request):
    breadcrumbs = {
        'dashboard' : {'name': 'Dashboard', 'url': 'app_dashboard:home'},
        'outlet' : {
            'index' : {'name': 'Outlets Overview', 'url': 'app_outlet:outletIndex'},
            'add' : {'name': 'Add Outlet'},
            'view' : {'name': 'View Outlet'},
            'update' : {'name': 'Update Outlet'},
        },
        'vehicle' : {
            'index' : {'name': 'Vehicle & Driver Overview', 'url': 'app_vehicle:vehicleIndex'},
            'add' : {'name': 'Add Vehicle'},
            'update' : {'name': 'Update Vehicle'},
        },
        'driver' : {
            'add' : {'name': 'Add Driver'},
            'view' : {'name': 'View Driver'},
            'update' : {'name': 'Update Driver'},
            },
        'schedule' : {
            'index' : {'name': 'Select Outlets', 'url':'app_schedules:index'},
            'view' : {'name': 'Confirm Selected Outlets', 'url':'app_schedules:viewoutlets'},
            'vehicle' : {'name': 'Select Vehicles', 'url':'app_schedules:vehicles'},
            'driver' : {'name': 'Select Drivers', 'url':'app_schedules:drivers'},
            'result' : {'name': 'Result'},

        },
        'report' : {
            'index': {'name': 'List of Report', 'url': 'app_report:index'},
            'view' : {'name': 'View Report'},
            'add' : {'name' : 'Add New Outlet'},
            'result' : {'name' : 'Result'}
        },
        # 'user' : {'name': 'Vehicles', 'url': 'app_user:index'},
        
    }
    return {
        'breadcrumbs': breadcrumbs
    }