from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from djoser.views import UserViewSet as DjoserUserViewSet

from api.pagination import PageLimitPagination
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet, ):
    pass

    # @action(methods=['get', 'post', 'delete'], detail=True)
    # def subscribe(self, request, id):
    #     return self.add_delete_relationships(id, conf.SUBSCRIBE_M2M)


