from django.urls import path
from users.views import sign_up,Login,Log_out
urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    path("login/",Login,name="login"),
    path("logout/",Log_out,name="logout"),
]
