from django import forms

from .models import Archer


class ArcherRegistrationForm(forms.ModelForm):
    class Meta:
        model = Archer
        exclude = ('user', 'date_register', 'religion', 'verified',
                   'approved', 'approved_by', 'region_code_name', 'qrcode')


class ArcherCompleteProfileForm(forms.ModelForm):
    class Meta:
        model = Archer
        fields = ('body_weight', 'body_height', 'draw_length')


class ArcherLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
