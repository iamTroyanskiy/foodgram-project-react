from django.urls import path, include
from rest_framework.routers import SimpleRouter

from recipes.views import TagViewSet, IngredientViewSet, RecipeViewSet

app_name = 'recipes'

router = SimpleRouter()
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
