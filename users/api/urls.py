from django.urls import path
from .views import UserCreateView, AuthToken, StatusCreateView
app_name = 'users'

urlpatterns = [
    path('', UserCreateView.as_view(), name='user-create'),
    path('auth-token', AuthToken.as_view(), name='auth-token'),
    path('status', StatusCreateView.as_view(), name='status-create')
]
