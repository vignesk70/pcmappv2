from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pcmappv2'
urlpatterns = [
    #display home page
    path('',views.IndexView.as_view(), name='index'),
    path('register/',views.RegisterMember.as_view(),name='registermember'),
    path('activities/',views.ActivitiesList.as_view(),name='activities'),
    path('bootstrap/',views.BootStrapView.as_view(),name='bootstrap'),

]
