from rest_framework.exceptions import ValidationError


def validate_id_values(value, model):
    if not value.isdecimal():
        raise ValidationError(
            f'{value} должно содержать цифру'
        )
    obj = model.objects.filter(id=value)
    if not obj:
        raise ValidationError(
            f'{value} не существует'
        )
    return obj[0]
