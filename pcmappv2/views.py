from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic
# Create your views here.

class IndexView(generic.TemplateView):
    template_name='pcmappv2/index.html'
