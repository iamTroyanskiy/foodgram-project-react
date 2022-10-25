from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer as DjoserUserSerializer
from rest_framework.fields import SerializerMethodField

from users.services import lower_normalize_value

User = get_user_model()


class CustomUserCreateSerializer(DjoserUserSerializer):

    def validate_username(self, value):
        return lower_normalize_value(
            model=User,
            field_name='username',
            field_value=value
        )

    def validate_email(self, value):
        return lower_normalize_value(
            model=User,
            field_name='email',
            field_value=value
        )

    def validate_first_name(self, value):
        return value.capitalize()

    def validate_last_name(self, value):
        return value.capitalize()


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

#
# class SubscribeUserSerializer(UserSerializer):
#     recipes = MiniRecipeSerializer(
#                 many=True,
#                 read_only=True,
#             )
#     recipes_count = SerializerMethodField(
#                 read_only=True,
#             )
#
#     class Meta(UserSerializer.Meta):
#         fields = UserSerializer.Meta.fields + (
#             'recipes',
#             'recipes_count',
#         )
