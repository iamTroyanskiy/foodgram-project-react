[![foodgram_workflow](https://github.com/tonik350/foodgram-project-react/actions/workflows/main.yml/badge.svg)](https://github.com/tonik350/foodgram-project-react/actions/workflows/main.yml)

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)

<h1 align="center">
  <br>
  <img src="https://github.com/tonik350/img/blob/main/logo.png?raw=true"  width="500"></a>
  <br>
    ПРОДУКТОВЫЙ ПОМОЩНИК
  <br>
</h1>

## Описание

Онлайн-сервис Foodgram и API для него.Имеется реализация CI/CD проекта.На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список "Избранное", а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Проект доступен по адресу [f00dgram.ddns.net](https://f00dgram.ddns.net)

### Доступный функционал

- Аутентификация реализована с помощью стандартного модуля DRF - Authtoken.
- У неаутентифицированных пользователей доступ к API только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям.На прочий фунционал наложено ограничение в виде административных ролей и авторства.
- Управление пользователями.
- Возможность получения подробной информации о себе и ее редактирование.
- Возможность подписаться на других пользователей и отписаться от них.
- Получение списка всех тегов и ингредиентов.
- Получение списка всех рецептов, их добавление.Получение, обновление и удаление конкретного рецепта.
- Возможность добавить рецепт в избранное.
- Возможность добавить рецепт в список покупок.
- Возможность скачать список покупок в PDF формате.
- Фильтрация по полям.


## Технологии

- Python 3.7
- Django 3.2.15
- Django Rest Framework 3.12.4
- Authtoken
- Docker
- Docker-compose
- PostgreSQL
- Gunicorn
- Nginx
- GitHub Actions
- Выделенный сервер Linux Ubuntu 22.04 с публичным IP

## Установка на сервер
- Клонировать репозиторий
```
git clone git@github.com:tonik350/foodgram-project-react.git
```
- Подключиться к серверу
```
ssh <server user>@<server IP>
```
- Установить Docker и Docker Compose на сервер
```
sudo apt install docker.io
sudo apt install docker-compose
```
- Проверить их работоспособность
```
sudo docker --version
sudo docker-compose --version
```
- Создать в домашней директории директорию 'foodgram'
```
mkdir foodgram && cd foodgram/
```
- Скопировать файлы из директории 'infra' (на локальной машине) в директорию 'infra' на сервере:
```
scp -r infra/* <server user>@<server IP>:/home/<server user>/foodgram/
```
- Создать в директории 'infra' env-файл
```
touch .env
```
- Заполнить env-файл
```
DEBUG=False
DJANGO_SECRET_KEY=<Your_some_long_string>
DB_ENGINE='django.db.backends.postgresql'
POSTGRES_DB='foodgram'
POSTGRES_USER='foodgram_user'
POSTGRES_PASSWORD=<Your_password>
DB_HOST='db'
DB_PORT=5432
```
- Запустить docker-compose
```
sudo docker-compose up -d
```

## Локальная установка
- Склонировать репозиторий и перейти в папку с проектом командами :
 ```
 git clone git@github.com:tonik350/foodgram-project-react.git
 ```
- Установить виртуальное окружение и активировать его:
```
 python3 -m venv venv
 ```
 ```
 source venv/bin/activate
 ```
- Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
- Выполнить миграции:
```
python3 manage.py migrate
```
- Запустить сервер командой
```
python3 manage.py runserver
```

## Примеры некоторых запросов API

Регистрация пользователя:

```bash
   POST /api/v1/users/
```

Получение данных своей учетной записи:

```bash
   GET /api/v1/users/me/ 
```

Добавление подписки:

```bash
   POST /api/v1/users/id/subscribe/
```

Обновление рецепта:
  
```bash
   PATCH /api/v1/recipes/id/
```

Удаление рецепта из избранного:

```bash
   DELETE /api/v1/recipes/id/favorite/
```

Получение списка ингредиентов:

```bash
   GET /api/v1/ingredients/
```

Скачать список покупок:

```bash
   GET /api/v1/recipes/download_shopping_cart/
```
