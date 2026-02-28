from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home(request):
    # work with databse
    # transfrom data data
    # data pass
    # http response / json response
    return HttpResponse("wellcome to the task management system")

def contact(request):
    return HttpResponse("<h1 style='color:red'>My name is raju</h1>")

def show_task(request):
    return HttpResponse("<h1 style='color:red'>My name is Rohan</h1>")