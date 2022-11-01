from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from api.mixins import AddDeleteManyToManyMixin
from api.pagination import PageLimitPagination
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet, AddDeleteManyToManyMixin):
    http_method_names = ['get', 'post', 'delete']
    add_delete_serializer = UserSerializer
    pagination_class = PageLimitPagination

    @action(
        detail=False,
        methods=[
            'get',
        ],
    )
    def subscriptions(self, request):
        user = self.request.user
        subscriptions = user.subscribes.all()
        pages = self.paginate_queryset(subscriptions)
        serializer = self.get_serializer(
            pages,
            many=True,
            context={'action': self.action}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=[
            'post',
            'delete',
        ],
    )
    def subscribe(self, request, id=None):
        if request.user == User.objects.get(pk=id):
            return Response(
                {'error': 'Нельзя подписаться на себя!'},
                status=HTTP_400_BAD_REQUEST
            )
        return self.add_delete_object(
            obj_id=id,
            field=request.user.subscribes
        )
