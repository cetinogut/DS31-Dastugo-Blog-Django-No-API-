"""dastugo_blog_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
   
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path("api/", include("dastugo_blog_api.urls", namespace="dastugo_blog_api")),
    path('api/user/', include('dastugo_user_app.urls', namespace='dastugo_user_app')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')), # API level auth screens  came via this route, this is built in by rest framwork to simulate user login etc.. We will use this end-points to login from REact
   
    path("blog/", include("dastugo_blog_app.urls", namespace="dastugo_blog_app")),
    path("users/", include("dastugo_user_app.urls")),
    path(
        "favicon.ico",
        RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),
    ),
    path('docs/', include_docs_urls(title='Dastugo-BlogAPI')),
    path('schema', get_schema_view(
        title="Dastugo-BlogAPI",
        description="API for the Dastugo Blog",
        version="1.0.0"
    ), name='openapi-schema'),
]


if settings.DEBUG: # use local media folder during development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
