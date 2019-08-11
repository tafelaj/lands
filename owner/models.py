# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from lrms.models import OwnerProfile
from django.contrib.auth.models import User

class Owner(OwnerProfile):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING())
