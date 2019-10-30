from django import forms

from orm import member as member_models


class MemberForm(forms.ModelForm):
    username = forms.CharField(max_length=45)
    password = forms.CharField(max_length=45, required=False)
    first_name = forms.CharField(max_length=45)
    last_name = forms.CharField(max_length=45)
    email = forms.CharField(max_length=45, required=False)
    club_id = forms.CharField(max_length=5)

    class Meta:
        model = member_models.Member
        exclude = ['user', 'club', 'date_register', ]
