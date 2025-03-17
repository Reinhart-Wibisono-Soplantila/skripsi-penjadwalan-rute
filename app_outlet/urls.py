from django.urls import path
from . import views

app_name="app_outlet"
urlpatterns = [
    path('', views.outlet_index, name='outletIndex'),
    path('create/', views.outlet_create, name='outletCreate'),
    path('update/<str:outletCode>', views.outlet_update, name='outletUpdate'),
    path('view/<str:outletCode>', views.outlet_view, name='outletView'),
    path('delete/<str:outletCode>', views.outlet_delete, name='outletDelete'),
]
