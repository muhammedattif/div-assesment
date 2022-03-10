
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Users Urls
    path('users', include('users.urls', 'users')),
    # Users APIs uRLS
    path('api/users/', include('users.api.urls', 'users-api')),
]


# Debug tool on Debug = True
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
