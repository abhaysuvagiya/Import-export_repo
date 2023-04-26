from django.urls import path
from .views import upload_file
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('upload_csv/', upload_file, name='upload_csv'),
    path('download_excel/', views.download_excel, name='download_excel'),
    path('register/', views.register,name='register'),
    path('login/',views.user_login,name='login'), 
    path('home/',auth_view.LogoutView.as_view(template_name="myapp/home.html"),name='logout'), 
    path('upload/',auth_view.LogoutView.as_view(template_name="myapp/upload.html"),name='upload'), 
]
