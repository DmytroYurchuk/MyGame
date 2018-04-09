"""Api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static

from django.conf import settings

from rest_framework.routers import DefaultRouter
from rest_framework_swagger.views import get_swagger_view

from game import views as game_views


# urls for API
router = DefaultRouter()
router.register(r"api/v1/game",
    game_views.GameView,
    base_name="game")
router.register(r"api/v1/player",
    game_views.PlayerView,
    base_name="player")

schema_view = get_swagger_view(
    title="Game Api",
    url="",
    patterns=router.urls)


urlpatterns = [
    url(r"^api/v1/$", schema_view)
] + router.urls

