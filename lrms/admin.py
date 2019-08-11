# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
# from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
# import the custom forms and models
from .forms import LandsUserCreationForm, LandsUserChangeForm
from .models import Property, LandsUser, Authority, OwnerProfile


# custom user to show up in admin
class CustomUserAdmin(UserAdmin):
    add_form = LandsUserCreationForm
    form = LandsUserChangeForm
    model = LandsUser
    list_display = ['username', 'password', ]


# Register your models here.
admin.site.register(LandsUser, CustomUserAdmin)
admin.site.register(Property)
admin.site.register(Authority)
admin.site.register(OwnerProfile)
