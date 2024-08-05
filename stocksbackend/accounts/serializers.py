from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    
    class Meta:
        fields = ['email', 'username',]

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True
    )

    class Meta:
        fields=('password',)
    
    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise serializers.ValidationError('Missing Data. Reset Password Not Allowed.')

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = User.objects.filter(pk=pk).first()

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError('Incorrect Data. Reset Password Not Allowed.')

        user.set_password(password)
        user.save()
        return data

