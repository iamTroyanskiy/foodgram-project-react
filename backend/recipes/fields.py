from drf_extra_fields import fields
from rest_framework.fields import ImageField


class CustomBase64ImageField(fields.Base64ImageField):
    def to_representation(self, value):
        return ImageField.to_representation(self, value)
