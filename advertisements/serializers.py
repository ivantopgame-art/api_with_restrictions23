from django.contrib.auth.models import User
from rest_framework import serializers

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user
        return super().create(validated_data)

    def validate(self, data):
        instance = self.instance
        new_status = data.get('status', instance.status if instance else 'OPEN')

        if new_status != Advertisement.STATUS_OPEN:
            return data

        user = self.context['request'].user
        open_count = Advertisement.objects.filter(
            creator=user,
            status=Advertisement.STATUS_OPEN,
        ).count()

        if instance and instance.status == Advertisement.STATUS_OPEN:
            open_count -= 1

        if open_count >= 10:
            raise serializers.ValidationError(
                'У вас уже 10 открытых объявлений. Закройте одно, прежде чем создавать новое.'
            )

        return data
