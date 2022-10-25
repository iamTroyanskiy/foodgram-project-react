from rest_framework import serializers


def lower_normalize_value(model, field_name, field_value):
    normalize_value = field_value.lower()
    if model.objects.filter(**{field_name: normalize_value}).exists():
        raise serializers.ValidationError(
            f'Пользователь с таким {field_name} уже существует'
        )
    return normalize_value
