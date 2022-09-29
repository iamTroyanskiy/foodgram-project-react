from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.db import models

from users.enums import Roles


class CustomUser(AbstractUser):

    username_validator = RegexValidator(
        regex=r'^(?!me)[\w.@+-]+\Z',
        message=(
            "Username должен содержать только буквы, "
            "цифры и символы: '@', '.', '+', '-'. "
            "Запрещается использовать 'me'."
        ),
    )

    username = models.CharField(
        unique=True,
        max_length=150,
        validators=[username_validator, ],
        help_text=(
            "От 3 до 150 символов. "
            "Буквы, цифры и символы: '@', '.', '+', '-', '_'. "
            "Запрещается использовать в качестве username 'me'."
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
    role = models.CharField(
        max_length=Roles.max_len(),
        choices=Roles.get_choices(),
        default=Roles.USER.name.lower(),
        verbose_name='Уровень доступа',
    )
    subscribe = models.ManyToManyField(
        verbose_name='Подписки',
        related_name='subscribers',
        to='self',
        symmetrical=False,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', ]
    # @property
    # def is_admin(self):
    #     return self.role == Roles.ADMIN.name.lower()
    #
    # @property
    # def is_user(self):
    #     return self.role == Roles.USER.name.lower()

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username



# class Follow(models.Model):
#     user = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         related_name='followers',
#         verbose_name='Подписчик',
#         null=True
#     )
#     following = models.ForeignKey(
#         CustomUser,
#         on_delete=models.CASCADE,
#         related_name='following',
#         verbose_name='Автор',
#         null=True
#     )
#
#     class Meta:
#         constraints = (
#             models.UniqueConstraint(
#                 fields=('user', 'following'),
#                 name='unique_follow'),
#         )
