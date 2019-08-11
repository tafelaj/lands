from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import (Home, PropertyDetail, Landing)

app_name = 'owner'

urlpatterns =[
    # url(r'^login/$', auth_views.LoginView.as_view(), name='owner_login'),
    url(r'^$', Landing.as_view(), name='landing'),
    url(r'^(?P<owner_pk>[0-9]+)/$', Home.as_view(), name='owner_home'),
    url(r'^property/(?P<pk>[0-9]+)/$', PropertyDetail.as_view(), name='property_detail')
]