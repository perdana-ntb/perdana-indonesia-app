from orm.region import Region
from orm.club import Branch
from django import forms


class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'


class BranchForm(forms.ModelForm):
    region_id = forms.CharField(max_length=10)

    class Meta:
        model = Branch
        exclude = ['region', ]
