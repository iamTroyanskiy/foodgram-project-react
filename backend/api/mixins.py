from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)


class AddDeleteManyToManyMixin:

    def __init__(self):
        self.queryset = None
        self.request = None
        self.add_delete_serializer = None

    def add_delete_object(self, obj_id, field):
        obj = get_object_or_404(self.queryset, id=obj_id)
        serializer = self.add_delete_serializer(
            obj,
            context={'request': self.request}
        )
        obj_exist = field.filter(id=obj_id).exists()
        if (self.request.method == 'POST') and not obj_exist:
            field.add(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)
        if self.request.method == 'DELETE' and obj_exist:
            field.remove(obj)
            return Response(status=HTTP_204_NO_CONTENT)
        return Response(status=HTTP_400_BAD_REQUEST)
