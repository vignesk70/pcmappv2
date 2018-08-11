from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.views import generic
from .forms import NewMemberRegistrationForm, CarRegistrationFormSet, PaymentFormSet
from django.core.files.storage import FileSystemStorage

# Create your views here.

class IndexView(generic.TemplateView):
    template_name='pcmappv2/index.html'

class RegisterMember(generic.FormView):
    template_name='pcmappv2/registermember.html'
    form_class=NewMemberRegistrationForm
    success_url = 'success'

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        car_form = CarRegistrationFormSet()
        receipt_form = PaymentFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  car_form=car_form,
                                  receipt_form=receipt_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        car_form = CarRegistrationFormSet(self.request.POST)
        receipt_form = PaymentFormSet(self.request.POST, self.request.FILES)
        if (form.is_valid() and car_form.is_valid() and receipt_form.is_valid()):
            return self.form_valid(form, car_form, receipt_form)
        else:
            return self.form_invalid(form, car_form, receipt_form)

    def form_valid(self, form, car_form, receipt_form):
        self.object = form.save()
        car_form.instance = self.object
        car_form.save()
        receipt_form.instance = self.object
        receipt_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, car_form,receipt_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  car_form=car_form,
                                  receipt_form=receipt_form))


class NewMemberRegistationSuccess(generic.TemplateView):
    template_name='pcmappv2/registrationsuccess.html'


class ActivitiesList(generic.TemplateView):
    template_name='pcmappv2/activities.html'

class SCCheck(generic.TemplateView):
    template_name='pcmappv2/sccheck.html'
# class BootStrapView(generic.FormView):
#     template_name='pcmappv2/bootstrap.html'
#     form_class=BootstrapForm
