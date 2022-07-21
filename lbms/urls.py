"""lbms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from library_store.views.logout.api_wrapper import LogoutAPI
from library_store.views.register.api_wrapper import RegisterAPI

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register', RegisterAPI.as_view()),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name='login_refresh'),
    path('logout', LogoutAPI.as_view(), name='auth_logout'),
]
