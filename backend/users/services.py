from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


def normalize_fields(
        data,
        fields_to_lower_normalize,
        fields_to_capitalize_normalize
):
    for field in fields_to_lower_normalize:
        data[field] = data[field].lower()
    for field in fields_to_capitalize_normalize:
        data[field] = data[field].capitalize()
    return data


def validate_unique(field_name, field_value):
    icontains_field_name = field_name + '__icontains'
    if User.objects.filter(**{icontains_field_name: field_value}).exists():
        raise serializers.ValidationError(
            f'Пользователь с таким {field_name} уже существует'
        )
