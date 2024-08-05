from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, tokens
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse

from .serializers import ForgetPasswordSerializer, ResetPasswordSerializer

# Create your views here.
class SignUpView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        user = User(username = username)
        user.set_password(password)
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

class SignInView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'username': user.get_username(), 
                'token': token.key,
                }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class ForgetPasswordView(generics.GenericAPIView):
    serializer_class = ForgetPasswordSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid(): return Response({"message": "Incorrect Details."}, status=status.HTTP_404_NOT_FOUND)
        username = serializer.data["username"]
        user = User.objects.filter(username=username).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = tokens.PasswordResetTokenGenerator().make_token(user=user)

            reset_url = reverse(
                'reset-password',
                kwargs={"encoded_pk": encoded_pk, "token" : token}
            )

            return Response({"uri" : reset_url}, status=status.HTTP_200_OK)
        return Response({"data" : "USER DOES NOT EXIST"}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs": kwargs})

        serializer.is_valid(raise_exception=True)

        return Response(
            {"data": "Password Reset Complete."},
            status= status.HTTP_202_ACCEPTED
        )