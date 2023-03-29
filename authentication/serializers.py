from rest_framework import serializers
from rest_framework.settings import api_settings

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password

from django.core.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


User = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']


class UserRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    password_confirm = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['username','email','password','password_confirm']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if len(username) < 6:
            raise serializers.ValidationError({
                "error":"Username must be of 6 or more characters"
            })
        if not username.isalnum():
            raise serializers.ValidationError({
                "error":"username must be alpha numeric"
            })
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({
                "error":f"user with username {username} already exists"
            })
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({
                "error":f"user with email {email} already exists"
            })
        if password != password_confirm:
            raise serializers.ValidationError({
                "error":"password does not match"
            })
        user = User(username=username, email=email)
        try:
            validate_password(password=password, user=user)
        except ValidationError as e:
            serializers_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError({
                "error":serializers_error[api_settings.NON_FIELD_ERRORS_KEY]
            })
        return attrs

    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    email = serializers.EmailField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id','username','password','email','access_token','refresh_token']
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"error":"invalid credentials"})
        if not user.is_active:
            raise serializers.ValidationError({"error":"user not active"})
        
        token = user.get_tokens()
        update_last_login(None ,user=user)
        return {
            'email':user.email,
            'username':user.username,
            'access_token':token['access'],
            'refresh_token':token['refresh'],
        }
    

class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs
    
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise serializers.ValidationError({
                "error":"Bad Token"
            })
