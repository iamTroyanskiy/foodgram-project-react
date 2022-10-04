"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_api.urls', namespace='api_auth')),
    path('api/', include('users.urls', namespace='api_users')),
    path('api/', include('recipes.urls', namespace='recipes')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# from django.contrib import admin
#
# from django.views.generic import TemplateView
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path(
#         'redoc/',
#         TemplateView.as_view(template_name='redoc.html'),
#         name='redoc'
#     ),
#     path('api/v1/auth/', include('api.urls', namespace='api')),
#     path('api/v1/', include('reviews.urls', namespace='api_reviews')),
#     path('api/v1/', include('users.urls', namespace='api_users')),
# ]
