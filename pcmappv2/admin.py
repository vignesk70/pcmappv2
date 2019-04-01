from django.contrib import admin

# Register your models here.
from .models import Member,Car,Payment,Activity
admin.AdminSite.site_header='Peugeot Club Administration'

class PaymentInLine(admin.TabularInline):
    model = Payment
    extras = 1

class CarInLine(admin.TabularInline):
    model = Car
    search_fields = ['car.car_reg_no']
    choices =1

class MemberAdmin(admin.ModelAdmin):
    search_fields = ['member_name','member_address_state',]
    list_display = ('member_name','member_since','member_expiry_date','member_phone','owner','member_address_state','member_status',)
    inlines = [CarInLine,PaymentInLine]

class CarAdmin(admin.ModelAdmin):
    list_display=('car_reg_no','member_id','car_model')
    search_fields=('member_id__member_name','car_reg_no',)

admin.site.register(Member,MemberAdmin)
admin.site.register(Car,CarAdmin)
admin.site.register(Payment)
admin.site.register(Activity)
