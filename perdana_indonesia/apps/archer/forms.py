from django import forms

from .models import Archer, ArcherApprovalDocument


class ArcherRegistrationForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField()
    public_photo = forms.ImageField()
    identity_card_photo = forms.ImageField()

    class Meta:
        model = Archer
        exclude = (
            'user', 'role', 'date_register', 'religion',
            'region_code_name', 'qrcode'
        )


class ArcherCompleteDocumentForm(forms.ModelForm):
    class Meta:
        model = ArcherApprovalDocument
        fields = ('skck', 'latsar_certificate')


class ArcherLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
