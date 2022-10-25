from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.core.validators import MinLengthValidator


class CustomUser(AbstractUser):
    username_validator = RegexValidator(
        regex=r'^[\w.@+-]+\Z',
        message=(
            "Username должен содержать только буквы, "
            "цифры и символы: '@', '.', '+', '-'. "
        ),
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[
            username_validator,
            MinLengthValidator(3)
        ],
        help_text=(
            "От 3 до 150 символов. "
            "Буквы, цифры и символы: '@', '.', '+', '-', '_'. "
        ),
        error_messages={
            'unique': 'Пользователь с таким username уже существует',
        }
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        error_messages={
            'unique': 'Пользователь с таким email уже существует',
        }
    )
    password = models.CharField(
        max_length=128,
        verbose_name='Пароль',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='150 символов или меньше',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='150 символов или меньше',
    )
    subscribes = models.ManyToManyField(
        verbose_name='Подписки',
        related_name='subscribers',
        to='self',
        symmetrical=False,
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
