from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic
from .forms import BootstrapForm
# Create your views here.

class IndexView(generic.TemplateView):
    template_name='pcmappv2/index.html'

class RegisterMember(generic.FormView):
    template_name='pcmappv2/registermember.html'
    form_class=BootstrapForm

class ActivitiesList(generic.TemplateView):
    template_name='pcmappv2/activities.html'

class BootStrapView(generic.FormView):
    template_name='pcmappv2/bootstrap.html'
    form_class=BootstrapForm
