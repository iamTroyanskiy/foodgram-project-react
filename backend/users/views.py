from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from djoser.views import UserViewSet as DjoserUserViewSet

from api.mixins import AddDeleteM2MMixin
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(DjoserUserViewSet, AddDeleteM2MMixin):
    http_method_names = ['get', 'post', 'delete']
    add_delete_serializer = UserSerializer

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
    def subscribe(self, request, pk=None):
        return self.add_delete_object(
            obj_id=pk,
            field=request.user.subscribes
        )
