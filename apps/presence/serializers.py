from rest_framework import serializers

from core.exceptions import PerdanaError
from orm import presence as presence_models


class BasePresenceContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = presence_models.PresenceContainer
        fields = '__all__'

    @property
    def request(self):
        return self.context.get('request')

    def create(self, validated_data):
        return presence_models.PresenceContainer.objects.create(**validated_data, creator=self.request.user.member)


class PresenceContainerSerializer(BasePresenceContainerSerializer):
    def to_representation(self, instance):
        reps = super().to_representation(instance)
        reps['presence_items'] = PresenceItemSerializer(instance.presence_items.all(), many=True).data
        return reps


class PresenceItemMemberSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField()

    def to_representation(self, instance):
        reps = super().to_representation(instance)
        reps['member_id'] = instance.user.username
        reps['photo'] = instance.photo.url if instance.photo else ''
        reps['public_photo'] = instance.public_photo.url if instance.public_photo else ''
        return reps


class PresenceItemSerializer(serializers.ModelSerializer):
    member = PresenceItemMemberSerializer()

    class Meta:
        model = presence_models.PresenceItem
        fields = '__all__'
