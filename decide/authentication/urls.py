from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import *


from django.urls import include, path

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('login/', obtain_auth_token),
    path('logout/', LogoutView.as_view()),
    path('getuser/', GetUserView.as_view()),
    path('register/', RegisterView.as_view())   
]
