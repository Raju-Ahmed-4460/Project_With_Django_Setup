from django.http import HttpResponse
from django.shortcuts import render
from tasks.forms import TaskForm,TaskModelForm
from tasks.models import Employee,Task

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
    ## give me all data from task model
    tasks=Task.objects.all()

    ## for the specific task

    task2=Task.objects.get(id=2) ## get sudhu matro akata data niya kaj kora akadik data thakle error diba

    ## for the first task
    first_task=Task.objects.first
    return render(request,"show_task.html",{'key':tasks,'task2':task2,'first_task':first_task})

    



