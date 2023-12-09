from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        # from django.core.mail import send_mail
        # from django.conf import settings
        # subject = "Account verification code"
        # message = "Thank you for registering, Your account verification code is 1234."
        #
        # send_mail(
        #     subject,
        #     message,
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=[user.email]
        # )
        return user
