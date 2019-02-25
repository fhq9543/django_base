from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register('register', views.UserRegisterAPIView, base_name='register')
router.register('server', views.ServerAPIView, base_name='server')

urlpatterns = [
    path('', include(router.urls)),
]
