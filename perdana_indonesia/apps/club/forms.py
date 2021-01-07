from django import forms

from club.models import Club


class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        exclude = ('central', 'province_code', 'city_code', 'district_code')
