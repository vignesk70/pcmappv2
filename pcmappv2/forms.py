from django import forms
from django.forms.models import inlineformset_factory
from .models import Member, Car, Payment


class NewMemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_name', 'member_email', 'member_phone', 'member_birthdate', 'member_address_state',
                  'member_address_postcode', 'member_on_chat', 'member_source', 'member_pdpa_accepted']
        widgets = {
            'member_birthdate': forms.DateInput(attrs={'type': 'date', 'format': 'YYYY-MM-DD'}),
            'member_name': forms.TextInput(attrs={'size': 50}),
            'member_email': forms.TextInput(attrs={'size': 50}),
            'member_address_postcode': forms.TextInput(attrs={'size': 5}),
            'member_on_chat': forms.NullBooleanSelect(attrs=None),
            'member_pdpa_accepted': forms.NullBooleanSelect(attrs=None),
        }


CarRegistrationFormSet = inlineformset_factory(Member,
                                               Car,
                                               fields=[
                                                   'member_id', 'car_reg_no', 'car_model', 'car_primary_sec'],
                                               can_delete=False,
                                               extra=1)

PaymentFormSet = inlineformset_factory(Member,
                                       Payment,
                                       fields=['payment_date', 'payment_amount',
                                               'payment_type', 'payment_receipt_image'],
                                       extra=1,
                                       can_delete=False,
                                       widgets={'payment_date': forms.DateInput(attrs={'type': 'date', 'format': 'YYYY-MM-DD'})})


class SCCheckForm(forms.Form):
    car_reg_no = forms.CharField(
        label='Car Registration Number', max_length=10)

    def clean_car_reg_no(self):
        car_reg_no = self.cleaned_data['car_reg_no']
        car_reg_no = car_reg_no.replace(" ", "")
        try:
            obj = Car.objects.filter(car_reg_no=car_reg_no)
            return car_reg_no
        except Car.DoesNotExist:
            raise forms.ValidationError('No record found')


class MembershipRenewForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_car_reg_no', 'payment_date',
                  'payment_amount', 'payment_type', 'payment_receipt_image']
        widgets = {'payment_date': forms.DateInput(
            attrs={'type': 'date', 'format': 'YYYY-MM-DD'})}
        exclude = ['payment_car_reg_no']


class EditMemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['member_name', 'member_email', 'member_phone', 'member_birthdate', 'member_address_state',
                  'member_address_postcode', 'member_on_chat', 'member_source', 'member_pdpa_accepted']
        widgets = {
            'member_birthdate': forms.DateInput(attrs={'type': 'date', 'format': 'YYYY-MM-DD'}),
            'member_name': forms.TextInput(attrs={'size': 50, 'readonly': 'True'}),
            'member_email': forms.TextInput(attrs={'size': 50, 'readonly': 'True'}),
            'member_address_postcode': forms.TextInput(attrs={'size': 5}),
            'member_on_chat': forms.NullBooleanSelect(attrs=None),
            'member_pdpa_accepted': forms.NullBooleanSelect(attrs=None),
        }
