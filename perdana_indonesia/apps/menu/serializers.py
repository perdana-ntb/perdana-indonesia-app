from rest_framework import serializers
from .models import AppMenu


class AppMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppMenu
        exclude = ('allowed_roles', )
