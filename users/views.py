from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm,CustomRegistrationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse

# Create your views here.
def sign_up(request):
    

    if request.method=="POST":
        form= CustomRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()


            messages.success(request,"Sign Up successfully")
            

    else:
        form= CustomRegistrationForm()

    return render(request,'registration/register.html',{"form":form})



def Login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Login Failed")
        
    
    return render(request,"registration/login.html")


def Log_out(request):
    if request.method=="POST":
        logout(request)
        return redirect('login')



