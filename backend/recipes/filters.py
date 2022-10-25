from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters

from rest_framework.filters import SearchFilter

from recipes.models import Tag, Recipe

User = get_user_model()


class RecipeFilter(filters.FilterSet):
    is_in_shopping_cart = filters.ChoiceFilter(
        choices=enumerate([0, 1]),
        method='filter_is_in_shopping_cart'
    )
    is_favorited = filters.ChoiceFilter(
        choices=enumerate([0, 1]),
        method='filter_is_favorited'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if int(value) == 1:
            return queryset.filter(shopping_cart=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if int(value) == 1:
            return queryset.filter(favorite=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags')


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'
