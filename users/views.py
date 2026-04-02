from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def sign_up(request):
    if request.method=='GET':
        form= UserCreationForm()

    if request.method=="POST":
        form= UserCreationForm(request.POST)
        form.is_valid()
        form.save()

    return render(request,'registration/register.html',{"form":form})