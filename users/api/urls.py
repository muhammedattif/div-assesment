from django.urls import path
from .views import UserCreateView, AuthToken, StatusCreateView, EncrypedAuthToken
app_name = 'users'

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-create'),
    path('auth-token', AuthToken.as_view(), name='auth-token'),
    path('custom-auth-token', EncrypedAuthToken.as_view(), name='custom-auth-token'),
    path('status', StatusCreateView.as_view(), name='status-create')
]
