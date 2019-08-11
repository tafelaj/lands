# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# imports for custom user
from django.contrib.auth.models import AbstractUser


GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
)
RELATION = (
    ('gma', 'Grand Mother'),
    ('gda', 'Grand Father'),
    ('dad', 'Father'),
    ('mom', 'Mother'),
    ('sis', 'Sister'),
    ('bro', 'Brother'),
    ('unc', 'Uncle'),
    ('aun', 'Auntie'),
    ('cuz', 'Cousin'),
    ('son', 'Son'),
    ('dot', 'Daughter'),
)
PROPERTY_TYPE = (
    ('R', 'Residential'),
    ('C', 'Commercial'),
)
PAYMENT_TYPES = (
    ('RNT', 'Payment for Land Rentals'),
    ('NO', 'New Occupancy'),
    ('OLR', 'Old Land Record'),
    ('PF', 'Penalty Fees'),
)


class OwnerProfile(models.Model):
    first_name = models.CharField(max_length=20, blank=False, null=False, default='John')
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=False, null=False, default='Nangoma')
    gender = models.CharField(max_length=1, choices=GENDER, default='')
    nrc = models.CharField(max_length=20, blank=False, null=False, unique=True)
    telephone = models.CharField(max_length=15, default='', null=True, blank=True)
    address = models.CharField(max_length=50, blank=False, null=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(verbose_name='Date of Birth', default=datetime.date(1995, 04, 13))

    @property
    def age(self):
        age = int((datetime.datetime.now().date() - self.date_of_birth).days / 365.25)
        return age

    def get_absolute_url(self):
        return reverse('owner-detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        owner_id = (str(self.first_name) + ' ' + str(self.middle_name) + ' ' + str(self.last_name))
        return owner_id


class Authority(models.Model):
    name = models.CharField(max_length=50)
    district = models.CharField(max_length=30)

    def __unicode__(self):
        return str(self.name)


class LandsUser(AbstractUser):
    man_number = models.CharField(max_length=20, default='-----', null=False, blank=False)
    phone = models.CharField(max_length=13, null=True, blank=True)
    local_authority = models.ForeignKey(Authority, on_delete=models.DO_NOTHING, null=True)
    position = models.CharField(max_length=20, null=False, blank=False, help_text="JOB TITLE")

    def __unicode__(self):
        return str(self.get_full_name()) + '-' + str(self.man_number) + '-' + str(self.local_authority)


class Property(models.Model):
    owner = models.ForeignKey(OwnerProfile, on_delete=models.DO_NOTHING, default=1, related_name='owner')
    # address = models.CharField(max_length=50, blank=False, null=False)  # probably redundant
    local_authority = models.CharField(max_length=50, blank=False, null=False)
    area = models.CharField(max_length=50, blank=False, null=False)
    holding_number = models.CharField(max_length=50, blank=False, null=False, unique=True)
    type = models.CharField(max_length=1, choices=PROPERTY_TYPE, blank=False, null=True, default='R')
    balance = models.FloatField(verbose_name='Balance Due')
    successor = models.CharField(max_length=50, blank=False, null=True)
    successor_relation = models.CharField(max_length=3, blank=False, null=True, choices=RELATION,
                                          verbose_name='Relationship With Next Of Kin', default='son')
    added_by = models.ForeignKey(LandsUser, on_delete=models.DO_NOTHING, null=True)
    added_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        property_id = (str(self.holding_number).upper() + ' - ' + str(self.area).upper())
        return property_id

    def get_absolute_url(self):
        return reverse('lrms:property_detail', kwargs={'pk': self.pk})


# land rate payments on property
class Payment(models.Model):
    received_from = models.ForeignKey(OwnerProfile, on_delete=models.DO_NOTHING,
                                      related_name='payer', default=1)  # auto fill
    received_by = models.ForeignKey(LandsUser, on_delete=models.DO_NOTHING)  # auto fill
    property = models.ForeignKey(Property, on_delete=models.DO_NOTHING)  # auto fill
    amount = models.FloatField()
    description = models.CharField(max_length=5, choices=PAYMENT_TYPES, blank=False, null=False, default='RNT')
    date = models.DateTimeField(auto_now_add=True)
    payment_number = models.CharField(max_length=50, default='elysian')  # auto generate payment number

    def generate_payment_number(self):
        plot_number = self.property.holding_number
        # number of payments made on this property
        payments_number = Payment.objects.filter(property=self.property).count()
        payment_number = str(plot_number) + str(self.description) + str(payments_number)
        return payment_number

    def __unicode__(self):
        payment = (str(self.received_from) + ' ' + str(self.property) + '-' + str(self.date))
        return payment

    def get_absolute_url(self):
        return reverse('lrms:payment_detail', kwargs={'pk': self.pk})
