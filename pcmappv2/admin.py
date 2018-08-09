from django.contrib import admin

# Register your models here.
from .models import Member,Car,Payment
admin.AdminSite.site_header='Peugot Club Administration'
admin.site.register(Member)
admin.site.register(Car)
admin.site.register(Payment)
