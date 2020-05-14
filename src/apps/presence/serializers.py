from rest_framework import serializers

from .models import PresenceContainer, PresenceItem


class BasePresenceContainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresenceContainer
        fields = '__all__'

    @property
    def request(self):
        return self.context.get('request')

    def create(self, validated_data):
        return PresenceContainer.objects.create(**validated_data, creator=self.request.user.member)


class PresenceContainerSerializer(BasePresenceContainerSerializer):
    def to_representation(self, instance):
        reps = super().to_representation(instance)
        reps['presence_items'] = PresenceItemSerializer(
            instance.presence_items.all(), many=True).data
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
        model = PresenceItem
        fields = '__all__'
