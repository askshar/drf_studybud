from django.urls import path

from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'register', views.UserViewSet, basename='register')

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('account-verify/', views.AccountVerifyView.as_view(), name='account-verify'),
] + router.urls
