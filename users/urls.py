from django.urls import path
from users.views import ProfileView, sign_up,Login,Log_out,Activate_user,CustomLoginView,Admin_dashboard,assign_role,create_group,group_data
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('sign-up/',sign_up,name='sign-up'),
    # path("login/",Login,name="login"),
    path("login/",CustomLoginView.as_view(),name="login"),
    # path("logout/",Log_out,name="logout"),
    path("logout/",LogoutView.as_view(),name="logout"),
    path("activate/<int:user_id>/<str:token>/",Activate_user),
    path("admin_dashboard/",Admin_dashboard,name='admin_dashboard'),
    path("admin/<int:user_id>/assignrole/",assign_role,name='assignrole'),
    path("admin/create_group/",create_group,name='create_group'),
    path("admin/group_data/",group_data,name="group_data"),
    path("profile/",ProfileView.as_view(template_name ="accounts/profile.html"))

    
]
