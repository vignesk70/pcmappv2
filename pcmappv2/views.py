from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.views import generic
from .forms import NewMemberRegistrationForm, CarRegistrationFormSet, PaymentFormSet,SCCheckForm, MembershipRenewForm
from django.core.files.storage import FileSystemStorage
from .models import Member,Payment,Car
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django import template
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import json
import urllib
import requests

# Create your views here.

def email(request):
    subject = 'New membership request from '+ request.member_name
    message = subject + '. Please login to the admin site to validate' # reverse('pcmappv2:sccheck_detail',args=[str(request.pk)])
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['info@peugeotclubmalaysia.com',]
    send_mail(subject,message,email_from,recipient_list)
    return True

def email_renew(request):
    subject = 'New membership request from '+ request.member_name
    message = subject + '. Please login to the admin site to validate' # reverse('pcmappv2:sccheck_detail',args=[str(request.pk)])
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['info@peugeotclubmalaysia.com',]
    send_mail(subject,message,email_from,recipient_list)
    return True


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

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        ''' End reCAPTCHA validation '''

        if (form.is_valid() and car_form.is_valid() and receipt_form.is_valid() and result['success']):
            return self.form_valid(form, car_form, receipt_form)
        else:
            return self.form_invalid(form, car_form, receipt_form)

    def form_valid(self, form, car_form, receipt_form):
        self.object = form.save()
        car_form.instance = self.object
        car_form.save()
        receipt_form.instance = self.object
        receipt_form.save()
        email(self.object)

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


class SCCheck(LoginRequiredMixin,generic.FormView):
    template_name='pcmappv2/sccheck.html'
    form_class=SCCheckForm
    success_url='detail'
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        #carid = get_object_or_404(Car, car_reg_no=request.POST.get('car_reg_no'))
        #self.success_url = 'sccheckdetails/%s' % carid.pk
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self,form):
        carid = Car.objects.get(car_reg_no=form.cleaned_data['car_reg_no'])
        self.success_url = 'detail/%s' % carid.pk
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self,form):
        return self.render_to_response(
            self.get_context_data(form=form))


class SCcheckDetailView(LoginRequiredMixin,generic.DetailView):
    model = Car
    template_name = 'pcmappv2/sccheck_detail.html'
    def get_context_data(self, **kwargs):
        context =  super(SCcheckDetailView, self).get_context_data(**kwargs)
        context['car'] = Car.objects.get(pk=self.kwargs.get('pk',None))
        context['member'] = Member.objects.get(id=context['car'].member_id.pk)
        return context


class MemberArea(LoginRequiredMixin,generic.TemplateView):
    template_name='pcmappv2/member_area.html'
    model=Member
    def get_context_data(self, **kwargs):
        context =  super(MemberArea, self).get_context_data(**kwargs)
        owner= self.request.user
        context['member'] = get_object_or_404(Member,owner=self.request.user)
        context['payment'] = Payment.objects.filter(payment_car_reg_no__owner=self.request.user)
        context['cars'] = Car.objects.filter(member_id=get_object_or_404(Member,owner=self.request.user))
        return context

class PCMMemberExpiring(LoginRequiredMixin,generic.ListView):
    template_name='pcmappv2/member_expiring.html'
    model=Member
    #queryset = Member.objects.select_related().filter(member_expiry_date__month=date.today().month,member_expiry_date__year=date.today().year)
    queryset = Member.objects.select_related().filter(member_expiry_date__lte=date.today(),member_status=True)

class MembershipRenew(LoginRequiredMixin,generic.FormView):
    template_name = 'pcmappv2/renewmember.html'
    model =  Payment
    form_class = MembershipRenewForm
    success_url = 'success'


    def get_context_data(self, **kwargs):
        context =  super(MembershipRenew, self).get_context_data(**kwargs)
        context['member'] = get_object_or_404(Member,owner=self.request.user)
        return context

    def get(self, request, *args, **kwargs):
        initial = {'payment_car_reg_no': get_object_or_404(Member,owner=self.request.user)}
        self.object = None
        form_class = self.get_form_class()
        form = self.form_class(initial=self.initial)
        #form = self.get_form(form_class)
        #form.instance.payment_car_reg_no = get_object_or_404(Member,owner=self.request.user)
        #form..payment_car_reg_no=get_object_or_404(Member,owner=self.request.user)
        return self.render_to_response(
            self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        #form = self.get_form(form_class)
        form = MembershipRenewForm(self.request.POST, self.request.FILES)
        #form['payment_car_reg_no']=self.request.user
        # ''' Begin reCAPTCHA validation '''
        # recaptcha_response = request.POST.get('g-recaptcha-response')
        # data = {
        #     'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        #     'response': recaptcha_response
        # }
        # r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        # result = r.json()
        #
        # ''' End reCAPTCHA validation '''

        if (form.is_valid() ): #and result['success']
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        payment= form.save(commit=False)
        payment.payment_car_reg_no = get_object_or_404(Member,owner=self.request.user)
        payment.save()
        #self.object = form.save()
        #email(payment)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))

class RenewSuccess(generic.TemplateView):
    template_name='pcmappv2/renewsuccess.html'

# class BootStrapView(generic.FormView):
#     template_name='pcmappv2/bootstrap.html'
#     form_class=BootstrapForm
