from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'rooms', views.RoomViewSet, basename='rooms')
router.register(r'messages', views.MessageViewSet, basename='messages')

urlpatterns = [
    path("", include(router.urls)),
]
