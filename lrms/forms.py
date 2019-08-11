from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import LandsUser, Property, OwnerProfile


class LandsUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = LandsUser
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'local_authority', 'man_number',)


class LandsUserChangeForm(UserChangeForm):

    class Meta:
        model = LandsUser
        fields = ('phone', 'email', 'local_authority',)


class OwnerForm(forms.ModelForm):
    class Meta:
        model = OwnerProfile
        fields = '__all__'


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
