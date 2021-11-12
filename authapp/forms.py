from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

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
    
    """def clean_age(self):
        data = self.cleaned_data['age']
        if data < 18:
            raise forms.ValidationError("Вы слишком молоды!")

        return data"""


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
