from django.contrib.auth import get_user_model
from django.db import IntegrityError
from djoser.serializers import UserCreateSerializer as DjoserUserSerializer
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

User = get_user_model()


class UserSerializer(DjoserUserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        DjoserUserSerializer.Meta.fields += ('is_subscribed', )
        # read_only_fields = (
        #     'id',
        #     'is_subscribed',
        # )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous or user == obj:
            return False
        a = user.subscribe.filter(id=obj.id).exists()
        return a


