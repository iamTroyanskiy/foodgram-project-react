from django.contrib import admin

from .models import Recipe, Tag, Ingredient, RecipeIngredient


class IngredientInLine(admin.StackedInline):
    model = Recipe.ingredients.through
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'author',
        'name',
        'pub_date',
        'image',
        'text',
        'cooking_time',
    )
    fields = (
        'author',
        'name',
        'pub_date',
        'image',
        'text',
        'cooking_time',
        'tags',
    )
    readonly_fields = ('pub_date',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'
    inlines = (IngredientInLine, )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'color',
        'slug',
    )
    search_fields = ('name', 'slug', 'color')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'measurement_unit',
    )
    search_fields = ('name', 'measurement_unit')
    empty_value_display = '-пусто-'

@admin.register(RecipeIngredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'recipes',
        'ingredients',
    )
    empty_value_display = '-пусто-'

#dmin.site.register(RecipeIngredient)
