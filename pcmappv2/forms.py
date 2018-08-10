from django import forms
from .models import Member, Car, Payment
<<<<<<< HEAD

class BootstrapForm(forms.ModelForm):
    class Meta:
        model=Member
        fields = ['member_name','member_email','member_phone','member_birthdate','member_address_state','member_address_postcode','member_on_chat','member_source']
        widgets = {
            'member_birthdate': forms.DateInput(attrs={'type': 'date', 'format' :'YYYY-MM-DD'}),
            'member_name' : forms.TextInput(attrs={'size':40}),
            'member_email' : forms.TextInput(attrs={'size':40}),
            'member_address_postcode' : forms.TextInput(attrs={'size':5}),
            'member_on_chat' : forms.NullBooleanSelect(attrs=None),
        }
=======
>>>>>>> 0e6477cd76d793651e559d5d017d2aaff30006eb
