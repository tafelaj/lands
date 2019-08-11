# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView
from . forms import OwnerForm, PropertyForm, LandsUserCreationForm
from . models import OwnerProfile, Property, Payment, LandsUser
from django.contrib.auth.models import User


class Home(TemplateView):
    template_name = 'lrms/home.html'

    # Search Views to find house number before making the payment.
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            query_list = None
            query = request.GET.get('q')

            if query:
                query_list = Property.objects.all()
                query_list = query_list.filter(holding_number__icontains=query)

        else:
            return redirect('lrms:cover')

        context = {
            'query_list': query_list,
        }

        return render(request, self.template_name, context)


class Cover(TemplateView):
    template_name = 'lrms/cover.html'


# Owner classes
# -------------------------------------------------------------------------------------
class OwnerDetail(DetailView):
    model = OwnerProfile
    template_name = 'lrms/owner_detail.html'


def add_owner(request, non_existing_owner):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OwnerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            form.save(commit=False)
            form.save()
            new_owner_pk = form.instance.pk
            # redirect to add property
            return redirect('lrms:property_add', owner_pk=new_owner_pk)
    # if GET request
    else:
        form = OwnerForm()
    context = {'non_existing_owner': non_existing_owner,
               'form': form}
    return render(request, 'lrms/owner_create.html', context)


def check_nrc(request):  # checking to see if an owner exists before adding a property to the database
    try:
        nrc = request.GET.get('nrc')
        owner = OwnerProfile.objects.get(nrc__exact=nrc)
        if owner:
            return redirect('lrms:property_add', owner_pk=owner.pk)

    except OwnerProfile.DoesNotExist:
        non_existing_owner = 1
        return redirect('lrms:add_owner', non_existing_owner=non_existing_owner)


# Property classes
# -------------------------------------------------------------------------------------
class PropertyAdd(CreateView):
    model = Property
    fields = ['holding_number', 'type', 'area', 'successor', 'successor_relation', ]

    def form_valid(self, form):
        # Getting the owner model
        try:
            owner = OwnerProfile.objects.get(pk=self.kwargs['owner_pk'])
        except OwnerProfile.DoesNotExist:
            return HttpResponse('Something went wrong, we couldn\'t find the owner you specified. Please try again')
        form.instance.owner = owner
        print owner
        form.instance.local_authority = self.request.user.local_authority
        print form.instance.local_authority
        form.instance.balance = 0.00
        print form.instance.balance
        form.instance.added_by = self.request.user
        print form.instance.added_by
        return super(PropertyAdd, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PropertyAdd, self).get_context_data(**kwargs)
        context['owner'] = OwnerProfile.objects.get(pk=self.kwargs['owner_pk'])
        return context

class PropertyUpdate(UpdateView):
    model = Property
    fields = ['owner']


class PropertyDetail(DetailView):
    model = Property
    template_name = 'lrms/property_detail.html'


class PropertyList(ListView):
    model = Property
    context_object_name = 'Properties'
    template_name = 'lrms/property_list.html'


class PropertyPage(TemplateView):
    template_name = 'lrms/property_page.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            plot = Property.objects.get(pk=self.kwargs['property_pk'])

            context = {'property': plot, }

            return render(request, self.template_name, context)
        else:
            return redirect('lrms:cover')


class OwnerPropertyList(TemplateView):
    template_name = 'lrms/owner_property_list.html'

    def get(self, request, *args, **kwargs):
        owner = OwnerProfile.objects.get(pk=self.kwargs['owner_pk'])
        queryset = Property.objects.filter(owner=owner)
        context = {
            'owner': owner,
            'queryset': queryset,
        }
        return render(request, self.template_name, context)


# classes for the payments
# ------------------------------------------------------------------------------------
class PaymentCreate(CreateView):
    model = Payment
    fields = ['amount', 'description']

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            plot = Property.objects.get(pk=self.kwargs['property_pk'])
            received_from = plot.owner

            form.instance.received_from = received_from
            form.instance.property = plot
            form.instance.received_by = self.request.user
            form.instance.payment_number = Payment.generate_payment_number(form.instance)
            plot.balance = (plot.balance - form.instance.amount)
            plot.save()
            return super(PaymentCreate, self).form_valid(form)

        else:
            return redirect('lrms:cover')


class PaymentDetail(DetailView):
    model = Payment
    template_name = 'lrms/payment_detail.html'


class PaymentHistory(TemplateView):
    template_name = 'lrms/payment_history.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            plot = Property.objects.get(pk=self.kwargs['property_pk'])
            payment_history = plot.payment_set.all()
            context = {
                'property': plot,
                'payment_history': payment_history,

            }
            return render(request, self.template_name, context)
        else:
            return redirect('lrms:cover')


# User CreateViews
class SignUp(CreateView):
    form_class = LandsUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class Tafela(View):

    def get(self, request, nangoma=None):
        plot = Property.objects.get(pk=nangoma)
        received_from = plot.owner
        # balance = plot.balance - (form.instance.amount)
        context = {
            'test': nangoma,
            'owner': received_from,
            'plot': plot,
            # 'balance': balance,
        }
        return render(request, 'lrms/test.html', context)


class LandsUserProfile(DetailView):
    model = LandsUser
    context_object_name = 'profile'
    template_name = 'lrms/lands_profile.html'
