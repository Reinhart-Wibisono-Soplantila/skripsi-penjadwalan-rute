from django.urls import path
from . import views

app_name='app_report'
urlpatterns = [
    path('', views.index, name='index'),
    path('view/<str:Schedule_id>', views.view, name='view'),
    path('maps/<str:Schedule_id>/<str:Vehicle_id>', views.maps, name='maps'),
    path('add-outlet/<str:Schedule_id>/<str:Vehicle_id>', views.add, name='add'),
    path('selected-outlets/process-outlets/', views.processoutlets, name='processoutlets'),
    path('new-schedule/result', views.result, name='result'),
    path('delete/<str:Schedule_id>', views.delete, name='delete')
]
