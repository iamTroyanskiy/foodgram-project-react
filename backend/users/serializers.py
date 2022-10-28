from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserSerializer as DjoserUserSerializer,
    UserCreateSerializer
)
from rest_framework.fields import SerializerMethodField

from users.services import normalize_fields, validate_unique

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        fields_to_lower_normalize = ('username', 'email')
        fields_to_capitalize_normalize = ('first_name', 'last_name')
        normalize_data = normalize_fields(
            data=data,
            fields_to_lower_normalize=fields_to_lower_normalize,
            fields_to_capitalize_normalize=fields_to_capitalize_normalize
        )
        return normalize_data

    def validate_username(self, value):
        validate_unique(
            field_name='username',
            field_value=value
        )
        return value

    def validate_email(self, value):
        validate_unique(
            field_name='email',
            field_value=value
        )
        return value


class UserSerializer(DjoserUserSerializer):
    is_subscribed = SerializerMethodField()

    class Meta(DjoserUserSerializer.Meta):
        fields = DjoserUserSerializer.Meta.fields + ('is_subscribed',)

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

        if self.context.get('action') == 'subscriptions':
            from recipes.serializers import RecipeMinifiedSerializer
            self.fields['recipes'] = RecipeMinifiedSerializer(
                many=True,
                read_only=True,
            )
            self.fields['recipes_count'] = SerializerMethodField(
                read_only=True,
            )

    def get_is_subscribed(self, obj):
        if self.context.get('action') == 'subscriptions':
            return True
        user = self.context.get('request').user
        if user.is_anonymous or user == obj:
            return False
        return user.subscribes.filter(id=obj.id).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()
