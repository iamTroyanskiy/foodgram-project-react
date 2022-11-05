from django.contrib.auth import get_user_model
from django.core.validators import (
    MinValueValidator,
    RegexValidator,
    MinLengthValidator
)
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=60,
        verbose_name='Название',
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единицы измерения',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                name='name_measurement_unit_unique',
                fields=('name', 'measurement_unit',)
            ),
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    hex_validator = RegexValidator(
        regex=r'^#[A-Fa-f0-9]{3,6}$',
        message=(
            'Введите валидный цветовой HEX-код!'
        )
    )

    name = models.CharField(
        max_length=60,
        verbose_name='Название',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        validators=[hex_validator, ],
        verbose_name='Цвет',
        help_text='Цветовой HEX-код (например, #49B64E).'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Имя автора',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        validators=[
            MinLengthValidator(3)
        ],
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        verbose_name='Изображение',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
        help_text='Продукты для приготовления блюда по рецепту',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэги',
        help_text='Можно установить несколько тегов на один рецепт',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, 'Минимальное значение: 1'),
        ],
        verbose_name='Время приготовления',
        help_text='Время приготовления в минутах'
    )
    favorite = models.ManyToManyField(
        User,
        related_name='favorites',
    )
    shopping_cart = models.ManyToManyField(
        User,
        related_name='shopping_cart',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        constraints = [
            models.UniqueConstraint(
                name='author_recipe_unique',
                fields=('author', 'name',)
            ),
        ]

    def __str__(self):
        return f'{self.name} by {self.author}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient_amount',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='amount_for_recipe',
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='recipe_ingredient_unique',
                fields=['recipe', 'ingredient'],
            ),
        ]
