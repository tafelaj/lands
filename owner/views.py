# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView, DetailView
from lrms.models import Property, OwnerProfile


class Home(TemplateView):

    template_name = 'owner/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            owner = OwnerProfile.objects.get(pk=self.kwargs['owner_pk'])
            plots = Property.objects.filter(owner=owner)

            context = {
                'property': plots,
                'owner': owner
                       }

            return render(request, self.template_name, context)
        else:
            return redirect('owner:owner_login')


class PropertyDetail(DetailView):
    model = Property
    template_name = 'owner/property_detail.html'


class Landing(TemplateView):
    template_name = 'owner/nrc_search.html'

    def get(self, request, *args, **kwargs):
        owner_pk = None
        query = request.GET.get('q')

        if query:
            try:
                owner = OwnerProfile.objects.get(nrc__icontains=query)
                owner_pk = owner.pk
                return redirect('owner:owner_home', owner_pk=owner_pk)

            except:
                print 'oho, fya pena nomba!!'

        context = {
                'query': query
            }
        return render(request, self.template_name, context)
