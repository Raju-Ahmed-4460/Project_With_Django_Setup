
from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test,create_form,view_task,update_form,delete_task
urlpatterns=[
    path('manager_dashboard/', manager_dashboard,name='manager_dashboard'),
    path('user_dashboard/', user_dashboard),
    path('test/',test),
    path('create_task/',create_form,name='create-task'),
    path('view_task/',view_task),
    path('update_task/<int:id>/',update_form,name='update-task'),
    path('delete_task/<int:id>/',delete_task,name='delete-task')
]