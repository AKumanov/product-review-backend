from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token


class ErrorHandler:
    _INVALID_PASSWORD1_ERROR_MESSAGE = "Password fields didn't match."
    _INVALID_PASSWORD2_ERROR_MESSAGE = "Old password is not correct."
    _AUTHORIZATION_ERROR = "You don't have permission for this user!"
    _EMAIL_EXISTS_ERROR_MESSAGE = 'This Email is already in use.'
    _USERNAME_EXISTS_ERROR_MESSAGE = 'Username is taken.'


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': True
            },
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password': "Password fields didn't match."
            })

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer, ErrorHandler):

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True
    )
    old_password = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    @classmethod
    def validate(cls, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({
                'password': "{}".format(ErrorHandler._INVALID_PASSWORD1_ERROR_MESSAGE)
            })
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({
                'old_password': "{}".format(ErrorHandler._INVALID_PASSWORD2_ERROR_MESSAGE)
            })

        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({
                'authorize': '{}'.format(ErrorHandler._AUTHORIZATION_ERROR)
            })

        instance.set_password(validated_data.get('password'))
        instance.save()

        return instance


class UpdateUserSerializer(serializers.ModelSerializer, ErrorHandler):

    email = serializers.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {
                'required': True
            },
            'last_name': {
                'required': True
            }
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({
                'email': '{}'.format(ErrorHandler._EMAIL_EXISTS_ERROR_MESSAGE)
            })
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({
                'email': '{}'.format(ErrorHandler._USERNAME_EXISTS_ERROR_MESSAGE)
            })
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({
                'authorize': '{}'.format(ErrorHandler._AUTHORIZATION_ERROR)
            })
        fields = ['first_name', 'last_name', 'email', 'username']
        for field in fields:
            setattr(instance, field, validated_data.get(field))

        instance.save()

        return instance
