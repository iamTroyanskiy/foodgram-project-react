import os
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from drf_pdf.renderer import PDFRenderer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.mixins import AddDeleteM2MMixin
from api.permissions import AdminAuthorOrReadOnly
from recipes.filters import RecipeFilter, IngredientSearchFilter
from recipes.models import Tag, Ingredient, Recipe
from recipes.serializers import (
    TagSerializer,
    RecipeSerializer,
    IngredientSerializer,
    RecipeMinifiedSerializer
)
from recipes.services import shopping_cart_to_pdf


class TagViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', )
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet, AddDeleteM2MMixin):
    http_method_names = ('get', 'post', 'patch', 'delete')
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    add_delete_serializer = RecipeMinifiedSerializer
    permission_classes = (AdminAuthorOrReadOnly,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=[
            'post',
            'delete',
        ],
    )
    def favorite(self, request, pk=None):
        return self.add_delete_object(
            obj_id=pk,
            field=request.user.favorites
        )

    @action(
        detail=True,
        methods=[
            'post',
            'delete',
        ],
    )
    def shopping_cart(self, request, pk=None):
        return self.add_delete_object(
            obj_id=pk,
            field=request.user.shopping_cart
        )

    @action(
        detail=False,
        methods=[
            'get'
        ],
        renderer_classes=(PDFRenderer,)
    )
    def download_shopping_cart(self, request):
        user = request.user
        file_path, file_name = shopping_cart_to_pdf(user)

        try:
            with open(file_path, 'rb') as pdf_file:
                response = HttpResponse(
                    FileWrapper(pdf_file),
                    content_type='application/pdf'
                )
                response['Content-Disposition'] = (
                    f'attachment; filename={file_name}'
                )
                return response

        finally:
            os.remove(file_path)


class IngredientViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', )
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('name',)
