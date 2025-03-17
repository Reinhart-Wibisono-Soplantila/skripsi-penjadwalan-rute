from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name='app_user'
urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='app_user:login'), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.profile, name='profile'),
    path('update/<str:userId>', views.update, name='userUpdate'),
    path('delete/<str:userId>', views.delete, name='userDelete'),
    path('index/', views.index, name='index'),
]