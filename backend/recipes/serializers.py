from django.contrib.auth import get_user_model
from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from rest_framework.validators import UniqueTogetherValidator

from users.serializers import UserSerializer
from .models import Tag, Recipe, Ingredient, RecipeIngredient
from .services import add_ingredients_to_recipe

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class RecipeTagSerializer(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        if self.pk_field is not None:
            return self.pk_field.to_representation(value.pk)
        return TagSerializer(value).data


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeMinifiedSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )
        read_only_fields = ('__all__',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        queryset=Ingredient.objects.all(),
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name',
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):

    tags = RecipeTagSerializer(
        many=True,
        queryset=Tag.objects.all(),
        allow_empty=False,
    )
    author = UserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    ingredients = RecipeIngredientSerializer(
        source='ingredient_amount',
        many=True
    )
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Recipe.objects.all(),
                fields=('author', 'name',),
                message='У вас уже есть рецепт с таким именем!'
            )
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredient_amount')
        recipe = Recipe.objects.create(**validated_data)
        ingredients_in_recipe = add_ingredients_to_recipe(
            ingredients_data,
            recipe
        )
        recipe.ingredient_amount.set(ingredients_in_recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients_data = validated_data.pop('ingredient_amount')
        recipe = super().update(recipe, validated_data)
        if ingredients_data:
            ingredients_in_recipe = add_ingredients_to_recipe(
                ingredients_data,
                recipe
            )
            recipe.ingredient_amount.set(ingredients_in_recipe, clear=True)
        if tags:
            recipe.tags.set(tags)
        return recipe

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(id=obj.id).exists()

    def validate_name(self, value):
        return value.capitalize()
