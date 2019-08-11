from django.conf.urls import url
from views import (Home, OwnerDetail, OwnerPropertyList, PropertyDetail, PaymentCreate, PaymentDetail, PropertyAdd, SignUp, Cover, Tafela,
                   PropertyList, PropertyPage, PaymentHistory, LandsUserProfile, check_nrc, add_owner)
from django.contrib.auth import views as auth_views

app_name = 'lrms'

urlpatterns = [
    # Auth URLs
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
    url(r'^password_change/done/$', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Misc URLs
    url(r'^$', Cover.as_view(), name='cover'),
    url(r'^home/$', Home.as_view(), name='home'),
    url(r'^profile/(?P<pk>[0-9]+)/', LandsUserProfile.as_view(), name='lands_user_profile'),
    # Property URLs
    url(r'property/add/(?P<owner_pk>[0-9]+)/$', PropertyAdd.as_view(), name='property_add'),
    url(r'^property/list/$', PropertyList.as_view(), name='property_list'),
    url(r'^property/(?P<pk>[0-9]+)/$', PropertyDetail.as_view(), name='property_detail'),
    url(r'^property/page/(?P<property_pk>[0-9]+)/$', PropertyPage.as_view(), name='property_page'),
    # payment URLs
    url(r'^payment/add/(?P<property_pk>[0-9]+)/$', PaymentCreate.as_view(), name='payment_add'),  # pk is for the property
    url(r'^payment/(?P<pk>[0-9]+)/$', PaymentDetail.as_view(), name='payment_detail'),
    url(r'^payment/history/(?P<property_pk>[0-9]+)/$', PaymentHistory.as_view(), name='payment_history'),
    # Tests
    url(r'^(?P<nangoma>\d+)/$', Tafela.as_view(), name='test'),
    # owner urls
    url(r'^property/check/$', check_nrc, name='nrc_check'),
    url(r'^owner/add/(?P<non_existing_owner>[0-9]+)/$', add_owner, name='add_owner'),
    url(r'^owner/(?P<pk>[0-9]+)/$', OwnerDetail.as_view(), name='owner_detail'),
    url(r'^owner/plotlist/(?P<owner_pk>[0-9]+)/$', OwnerPropertyList.as_view(), name='property_list_specific'),
]
