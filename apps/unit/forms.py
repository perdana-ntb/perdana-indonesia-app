from django import forms
from orm import club as club_models


class UnitForm(forms.ModelForm):
    class Meta:
        model = club_models.Unit
        exclude = ['branch', ]
