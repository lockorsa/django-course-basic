import datetime
import hashlib

import pytz
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, UserChangeForm,
)

from authapp.models import ShopUser


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fiels_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ShopUserRegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'birth_date':
                years_range = [year for year in range(2010, 1920, -1)]
                field.widget = forms.SelectDateWidget(years=years_range)

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.register_activation_key = hashlib.sha1(
            user.email.encode('utf8'),
            ).hexdigest()
        user.activation_key_expired = datetime.datetime.now(
            pytz.timezone(settings.TIME_ZONE),
        ) + datetime.timedelta(hours=48)
        user.save()
        return user

    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'password1',
            'password2',
            'email',
            'birth_date',
            'avatar',
        )


class ShopUserEditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()
            if field_name == 'birth_date':
                years_range = [year for year in range(2010, 1920, -1)]
                field.widget = forms.SelectDateWidget(years=years_range)

    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'password',
            'email',
            'birth_date',
            'avatar',
        )
