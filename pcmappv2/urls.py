from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pcmappv2'
urlpatterns = [
    #display home page
    path('',views.IndexView.as_view(), name='index'),
]
