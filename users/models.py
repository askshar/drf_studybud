from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from django_lifecycle import LifecycleModel, hook, AFTER_CREATE


class UserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Create and Saves user with given email and password
        :param email:
        :param password:
        :return: user instance
        """
        if not email:
            raise ValueError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email))
        user.is_staff = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        user.refresh_from_db(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Create and Saves superuser with given email and password
        :param email:
        :param password:
        :return: admin user instance
        """
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserCode(models.Model):
    user = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="user_codes")
    code = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    def save(self, *args, **kwargs):
        import random
        code = random.randint(10000, 99999)
        if self.pk is None:
            self.code = code
        super().save(*args, **kwargs)


class User(LifecycleModel, AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = models.CharField(
        max_length=25, unique=True,
        null=True, blank=True,
        validators=[UnicodeUsernameValidator(), ],
        error_messages={"unique": "User with that username already exists."}
    )
    email = models.EmailField(
        max_length=100, unique=True,
        error_messages={"unique": "User with that email already exists."}
    )
    is_verify = models.BooleanField(default=False)

    objects = UserManager()

    def __str__(self):
        if self.username:
            return self.username
        return self.email

    @hook(AFTER_CREATE)
    def generate_user_code(self):
        """
        Create and saves UserCode object (user code) for user verification
        after creating user instance.
        """
        code = UserCode.objects.create(user=self)
        self._send_verification_code(code)

    def _send_verification_code(self, code):
        from django.core.mail import send_mail
        from django.conf import settings
        subject = "Account verification code"
        message = f"Thank you for registering, Your account verification code for '{self.email}' is {code.code}."

        send_mail(
            subject,
            message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.email]
        )
        print("code ran successfully")
