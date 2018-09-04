# from django.contrib import admin
#
# # Register your models here.
# from .models import Member,Car,Payment
# admin.AdminSite.site_header='Peugeot Club Administration'
#
# class PaymentInLine(admin.TabularInline):
#     model = Payment
#     extras = 1
#
# class CarInLine(admin.TabularInline):
#     model = Car
#     search_fields = ['car.car_reg_no']
#     choices =1
#
# class MemberAdmin(admin.ModelAdmin):
#     search_fields = ['member_name']
#     list_display = ('member_name','member_since','member_expiry_date','member_phone','owner')
#     inlines = [CarInLine,PaymentInLine]
#
# admin.site.register(Member,MemberAdmin)
# admin.site.register(Car)
# admin.site.register(Payment)
