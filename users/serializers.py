from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import date
from django.conf import settings
from .models import Status

User = get_user_model()


"""
It is a Model serializer so the customization on the model Fields validators doesn't take effect.

"""


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'first_name', 'last_name', 'country_code', 'birth_date', 'gender', 'avatar', 'email')
        optional_fields = ['email', ]

    """
    All of these validation methods
    will be invoked only after passing the validation of the Model fields
    """

    def validate_first_name(self, first_name):
        if not first_name:
            raise serializers.ValidationError({'error': 'blank'})


    def validate_last_name(self, last_name):
        if not last_name:
            raise serializers.ValidationError({'error': 'blank'})


    # This validation vill not be invoked because I use Phone number field
    # which done the validation itself
    def validate_phone_number(self, phone_number):
        if len(phone_number) >= 15:
            raise serializers.ValidationError({'error': 'too_long', 'count': len(phone_number)})

        if len(phone_number) <= 10:
            raise serializers.ValidationError({'error': 'too_short', 'count': len(phone_number)})

    def validate_birth_date(self, birth_date):
        today = date.today()
        if birth_date > today:
            raise serializers.ValidationError("This Birth date in the future.")

    def validate_avatar(self, avatar):
        if avatar.name.split('.')[-1].lower() not in settings.VALID_IMAGE_EXT:
            raise serializers.ValidationError("Invalid image type.")

    def validate_email(self, email):
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")



class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('phone_number', 'status')

    def create(self, validated_data):
        user = self.context.get('user', None)
        validated_data['user'] = user
        status = Status.objects.create(**validated_data)  # saving status object
        return status

    def validate_phone_number(self, phone_number):
        user = self.context.get('user', None)
        if phone_number != user.phone_number:
            raise serializers.ValidationError("invalid")
        return phone_number

class AuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if not (phone_number or password):
            msg = 'Must include "phone_number" and "password"'
            raise serializers.ValidationError({
                'status': 'error',
                'message': msg
            })

        user = authenticate(phone_number=phone_number, password=password)

        if not user:
            msg = 'Unable to log in with provided credentials.'
            raise serializers.ValidationError({
                'status': 'error',
                'message': msg
            })

        if not user.is_active:
            msg = 'User account is disabled.'
            raise serializers.ValidationError({
                'status': 'error',
                'message': msg
            })


        attrs['user'] = user
        return attrs
