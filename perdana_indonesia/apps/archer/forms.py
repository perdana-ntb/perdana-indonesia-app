from django import forms

from .models import Archer


class ArcherRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField()
    public_photo = forms.ImageField()
    identity_card_photo = forms.ImageField()

    class Meta:
        model = Archer
        exclude = ('user', 'role', 'date_register', 'religion', 'region_code_name', 'qrcode')


class ArcherCompleteProfileForm(forms.ModelForm):
    class Meta:
        model = Archer
        fields = ('body_weight', 'body_height', 'draw_length')


class ArcherLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
