from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm,CustomRegistrationForm,CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator


# Create your views here.
def sign_up(request):
    if request.method=="POST":
        form= CustomRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active=False
            user.save()
            messages.success(request,"Check Your Mail")
            return redirect('login')
            
    else:
        form= CustomRegistrationForm()

    return render(request,'registration/register.html',{"form":form})



def Login(request):
    form = CustomLoginForm()

    if request.method == "POST":
        form = CustomLoginForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid or inactive account")

    return render(request, "registration/login.html", {'form': form})


def Log_out(request):
    if request.method=="POST":
        logout(request)
        return redirect('login')


def Activate_user(request, user_id, token):
    
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
          user.is_active = True
          user.save()
          return redirect('login')
        else:
            return HttpResponse("invalid id or token")
    except User.DoesNotExist:
        return HttpResponse("user not Found")



