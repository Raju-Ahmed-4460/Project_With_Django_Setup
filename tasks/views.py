from django.http import HttpResponse
from django.shortcuts import render,redirect
from tasks.forms import TaskForm,TaskModelForm,TaskDetailModelform
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Max,Min,Count,Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from users.views import is_admin

# Create your views here.

# user passes test  she or he is manager

def is_manager(user):
    return  user.groups.filter(name='manager').exists()

def is_employee(user):
    return  user.groups.filter(name='Employee').exists()


@user_passes_test(is_manager,login_url="no_permission")
def manager_dashboard(request):
    type = request.GET.get('type','all')
    
    # totak_count=tasks.count()
    # completed_task=Task.objects.filter(status="COMPLETED").count()
    # in_progress_task=Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task=Task.objects.filter(status="PENDING").count()


    counts=Task.objects.aggregate(
        totak_count=Count('id'),
        completed_task=Count('id',filter=Q(status='COMPLETED')),
        in_progress_task=Count('id',filter=Q(status='IN_PROGRESS')),
        pending_task=Count('id',filter=Q(status='PENDING')),
    )
    base_query=Task.objects.select_related("datils").prefetch_related("assigned_to") 


    # retriving data

    if type=='completed':
        tasks=base_query.filter(status='COMPLETED')
    elif type=='in_progress':
        tasks=base_query.filter(status='IN_PROGRESS')
    elif type=='pending':
        tasks=base_query.filter(status='PENDING')
    elif type=='all':
        tasks=base_query.all()

    contex={
        "tasks":tasks,
        "counts":counts,
    }
    return render(request, "dashboard/manager_dashboard.html",contex)


@user_passes_test(is_employee,login_url="no_permission")
def employee_dashboard(request):
    return render(request, "dashboard/user_dashboard.html")


def test(request):

    names=["raju","rohan","ruku"]
    count=0
    for name in names:
        count=count+1

    context={
        "names":names,
        "count":count
    }
    return render(request, "test.html",context)


## all are query in python format like databse sql query
@login_required
@permission_required('tasks.add_task',login_url="no_permission")
def create_form(request):
    # em = employee.objects.all()
    task_form =  TaskModelForm() ## for get request
    task_detail_form=TaskDetailModelform()

    if request.method == "POST":
        task_form =  TaskModelForm(request.POST) ## for get request
        task_detail_form=TaskDetailModelform(request.POST,request.FILES)
        if task_form.is_valid() and task_detail_form.is_valid():
            '''for modelform data'''
            task=task_form.save()
            task_detail=task_detail_form.save(commit=False)
            task_detail.task=task
            task_detail.save()
            messages.success(request,'task created successfully')
            return redirect('create-task')

            '''For django form data not modelform'''
            # data = form.cleaned_data

            # title = data.get('title')
            # description = data.get('description')
            # due_data = data.get('due_data')
            # assigned_to= data.get('assigned_to')
            # task=Task.objects.create(
            #     title=title,description=description,due_data=due_data
            # )

            # for emp_id in assigned_to:
            #     empl=employee.objects.get(id=emp_id)
            #     task.assigned_to.add(empl)
            # return HttpResponse("Sucessfully added")
               

    context = {"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request, "task_form.html", context)

@login_required
@permission_required('tasks.change_task',login_url="no_permission")
def update_form(request,id):
    # em = employee.objects.all()
    task=Task.objects.get(id=id)
    task_form =  TaskModelForm(instance=task) ## for get request
    if task.datils:
        task_detail_form=TaskDetailModelform(instance=task.datils)

    if request.method == "POST":
        task_form =  TaskModelForm(request.POST,instance=task) ## for get request
        task_detail_form=TaskDetailModelform(request.POST,instance=task.datils)
        if task_form.is_valid() and task_detail_form.is_valid():
            '''for modelform data'''
            task_form=task_form.save()
            task_detail_form.save()
            messages.success(request,'task updated successfully')
            return redirect('update-task',id)


    context = {"task_form": task_form,"task_detail_form":task_detail_form}
    return render(request, "task_form.html", context)



@login_required
@permission_required('tasks.delete_task',login_url="no_permission")
def delete_task(request,id):
    if request.method == "POST":
        task=Task.objects.get(id=id)
        task.delete()
        messages.success(request,'task delete successfully')
        return redirect('manager_dashboard')
    else:
        messages.error(request,'Somthing went  wrong')
        return redirect('manager_dashboard')




    

## See all Task
@login_required
@permission_required('tasks.view_task',login_url="no_permission")
def view_task(request):
    task_count=Task.objects.aggregate(num_task=Count('id'))

    return render(request,"show_task.html",{'task_count': task_count})






@login_required
@permission_required('tasks.view_task',login_url="no_permission")
def tasks_details(request,task_id):
    task=Task.objects.get(id=task_id)
    status_choices=Task.STATUS_CHOISES

    if request.method=="POST":
        select_status=request.POST.get('task_status')
        task.status=select_status
        task.save()
        return redirect('task_details',task.id)

    return render(request,"task_details.html",{'task':task,'status_choices':status_choices})



@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('user_dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')
    else:
        return redirect('no_permission')






    



