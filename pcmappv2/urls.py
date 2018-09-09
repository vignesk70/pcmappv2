from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.contrib import admin

app_name = 'pcmappv2'
urlpatterns = [
    #display home page
    path('',views.IndexView.as_view(), name='index'),
    path('register/',views.RegisterMember.as_view(),name='registermember'),
    path('activities/',views.ActivitiesList.as_view(),name='activities'),
    path('register/success/',views.NewMemberRegistationSuccess.as_view(),name='registrationsuccess'),
    path('sccheck/',views.SCCheck.as_view(),name='sccheck'),
    path('sccheck/detail/<int:pk>',views.SCcheckDetailView.as_view(),name='sccheck_detail'),
    path('member/',views.MemberArea.as_view(),name='member_area'),
    path('member/renew/<int:pk>',views.MembershipRenew.as_view(),name='member_renew'),
    path('member/renew/success',views.RenewSuccess.as_view(),name='renewalsuccess'),
    path('member/expiry',views.PCMMemberExpiring.as_view(),name='member_expiry'),
    path('accounts/', include('django.contrib.auth.urls')),
# path('bootstrap/',views.BootStrapView.as_view(),name='bootstrap'),
]
