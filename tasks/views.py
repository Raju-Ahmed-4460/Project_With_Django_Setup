from django.http import HttpResponse
from django.shortcuts import render
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task,TaskDetail,Project
from datetime import date
from django.db.models import Q,Max,Min,Count,Avg

# Create your views here.
def manager_dashboard(request):
    return render(request, "dashboard/manager_dashboard.html")

def user_dashboard(request):
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

def create_form(request):
    # em = employee.objects.all()
    form =  TaskModelForm() ## for get request

    if request.method == "POST":
        form = TaskModelForm(request.POST)

        if form.is_valid():
            '''for modelform data'''
            print(form)
            form.save()

            return render(request,'task_form.html',{'myform':form,'message':"Task Added successfully"})

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
               

    context = {"myform": form}
    return render(request, "task_form.html", context)

## See all Task

def view_task(request):
    # ## give me all data from task model
    # tasks=Task.objects.all()

    # ## for the specific task

    # task2=Task.objects.get(id=2) ## get sudhu matro akata data niya kaj kora akadik data thakle error diba

    # ## for the first task
    # first_task=Task.objects.first
    # return render(request,"show_task.html",{'key':tasks,'task2':task2,'first_task':first_task})
    # '''pending task'''
    # task=Task.objects.filter(status="PENDING")

    # """tody task """
    # tody_task=Task.objects.filter(due_data=date.today())

    # '''show the task whos priority is not low'''
    # task_hm=TaskDetail.objects.exclude(priority="L")
    # '''show the task whos priority is not high'''
    # task_hm=TaskDetail.objects.exclude(priority="H")


    '''sshow the the task that contain paper and status pending'''
    # task=Task.objects.filter(title__icontains="c" , status="PENDING")

    '''show the task where the status is pending or in progress'''

    # task=Task.objects.filter(Q(status="PENDING") | Q(status="IN_PROGRESSS"))

    '''kono data exists kora ki na'''

    # tasks=Task.objects.filter(status="PENDING").exists()


    """For One To One Ar JOIN THIS Is Two Way"""
    '''select related field(foregin key , one to one field)  join like query'''
    '''ata task theke datils ar access'''
    # tasks=Task.objects.select_related("datils").all()

    ''' akhon taskdatils thehe task ar access join query'''

    # tasks=TaskDetail.objects.select_related("task").all()



    """For Foregein key Join THIS IS one way"""
    '''Jamon amai task thehe project ke pabo but project thehe task ke bosate parbo na'''

    # tasks=Task.objects.select_related("project").all()

    """Prefetsch_relateted (many to mant and reverse foregein key)"""
    # tasks=Project.objects.prefetch_related('task_set').all()

    '''agrigation function'''
    task_count=Task.objects.aggregate(num_task=Count('id'))

    return render(request,"show_task.html",{'task_count': task_count})






    



