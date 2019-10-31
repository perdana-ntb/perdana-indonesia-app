from django import forms
from orm import club as club_models


class ClubForm(forms.ModelForm):
    class Meta:
        model = club_models.Club
        exclude = ['branch', ]
