from django.urls import path
from users.views import sign_up,Login,Log_out,Activate_user,Admin_dashboard,assign_role
urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    path("login/",Login,name="login"),
    path("logout/",Log_out,name="logout"),
    path("activate/<int:user_id>/<str:token>/",Activate_user),
    path("admin_dashboard/",Admin_dashboard,name='admin_dashboard'),
    path("admin/<int:user_id>/assignrole/",assign_role,name='assignrole')
    
]
