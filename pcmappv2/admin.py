from django.contrib import admin
from datetime import date
from import_export.admin import ImportExportModelAdmin, ImportExportMixin

# Register your models here.
from .models import Member, Car, Payment, Activity
admin.AdminSite.site_header = 'Peugeot Club Administration'


class PaymentInLine(admin.TabularInline):
    model = Payment
    extras = 1


class CarInLine(admin.TabularInline):
    model = Car
    search_fields = ['car.car_reg_no']
    choices = 1


class MemberAdmin(ImportExportMixin, admin.ModelAdmin):
    search_fields = ['member_name', 'member_address_state', ]
    list_display = ('member_name', 'member_since', 'member_expiry_date',
                    'member_phone', 'owner', 'member_address_state', 'member_status',)
    inlines = [CarInLine, PaymentInLine]


class CarAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('car_reg_no', 'member_id', 'car_model')
    search_fields = ('member_id__member_name', 'car_reg_no',)


class PaymentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ['payment_car_reg_no', 'payment_date',
                    'payment_amount', 'payment_updated_date', 'payment_updated_by']

    def save_model(self, request, obj, form, change):
        obj.payment_updated_by = request.user
        obj.payment_updated_date = date.today()
        super().save_model(request, obj, form, change)


admin.site.register(Member, MemberAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Activity)
