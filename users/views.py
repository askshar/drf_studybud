from django.contrib.auth import authenticate

from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserCode
from .serializers import UserSerializer


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is None:
            return Response(
                {"error": "Invalid Credentials!"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if user and not user.is_verify:
            return Response(
                {"user": "Your account is not verified, please verify first to login."},
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        response = {
            'id': user.id,
            'email': user.email,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny, ]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ["post"]


class AccountVerifyView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        if not email or not code:
            return Response({"required": "email and code is required."}, status=status.HTTP_400_BAD_REQUEST)

        user_code = UserCode.objects.filter(user__email=email, code=code).first()
        if not user_code:
            return Response(
                {"error": "Invalid email or code."},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found with this email id."},
                status=status.HTTP_404_NOT_FOUND
            )

        user.is_verify = True
        user.save()
        user_code.delete()
        return Response(
            {"success": "Your account has been verified, you can login now."},
            status=status.HTTP_200_OK
        )
