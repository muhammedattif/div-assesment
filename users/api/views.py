from users.serializers import UserSerializer, AuthTokenSerializer, StatusSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from django.conf import settings
from django.contrib.auth import get_user_model
from users.models import Status
from rest_framework.views import APIView
from rest_framework import status
import hashlib


User = get_user_model()

# User Creation View
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []


# Obtain Auth Token View
class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'phone_number': user.phone_number.raw_input
        })

# Generate encrypted Token based on phone number and password
class EncrypedAuthToken(APIView):

    permission_classes = []

    def post(self, request):

        serializer = AuthTokenSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=False)
        user = serializer.validated_data['user']
        phone_number = self.request.data['phone_number']
        password = self.request.data['password']

        plain_link = phone_number + password
        generated_token = hashlib.md5(plain_link.encode('utf-8'))

        return Response({
            'token': generated_token.hexdigest(),
            'user_id': user.pk,
            'phone_number': user.phone_number.raw_input
        })



# Status Creation View
class StatusCreateView(APIView):

    def post(self, request):
        serializer = StatusSerializer(data=self.request.data, context={'user': request.user})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'success': 'created'}, status=status.HTTP_201_CREATED)
