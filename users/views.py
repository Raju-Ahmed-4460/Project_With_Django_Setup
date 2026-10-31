from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from users.forms import RegisterForm,CustomPasswordResetConfirmForm,CustomPasswordResetForm,CustomRegistrationForm,CustomLoginForm,AssignRoleForm,CreateGroupForm,CustomPasswordChangeForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, permission_required,user_passes_test
from django.db.models import Prefetch
from django.contrib.auth.views import LoginView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from django.views.generic import TemplateView
from django.urls import reverse_lazy




# Create your views here.


# test user or admin
def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()



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


class CustomLoginView(LoginView):
    form_class=CustomLoginForm

    def get_success_url(self):
        next_url=self.request.GET.get("next")
        if next_url:
            return next_url
        else:
            return super().get_success_url()



class ChangePassword(PasswordChangeView):
    template_name="accounts/password_change.html"
    form_class=CustomPasswordChangeForm

        

@login_required
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
    
@user_passes_test(is_admin,login_url="no_permission")
def Admin_dashboard(request):
    users=User.objects.prefetch_related(
        Prefetch('groups',queryset=Group.objects.all(),to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name=user.all_groups[0].name
        else:
            user.group_name="no group assigned"
    return render(request,'admin/dashboard.html',{'users':users})


@user_passes_test(is_admin,login_url="no_permission")
def assign_role(request,user_id):
    form=AssignRoleForm()
    user=User.objects.get(id=user_id)

    if request.method=="POST":
        form=AssignRoleForm(request.POST)
        if form.is_valid():
            role=form.cleaned_data.get('role')
            user.groups.clear()
            user.groups.add(role)
            messages.success(request,f"role added for {user.username} to {role.name}")
            return redirect('admin_dashboard')
    

    return render(request,"admin/assignrole.html",{'form':form})
@login_required
@user_passes_test(is_admin,login_url="no_permission")
def create_group(request):
    form=CreateGroupForm()
    if request.method=="POST":
        form=CreateGroupForm(request.POST)

        if form.is_valid():
            group=form.save()
            messages.success(request,f"group{group.name} added successfully")
            return redirect('create_group')
    

    return render(request,"admin/creategroup.html",{'form':form})

@user_passes_test(is_admin,login_url="no_permission")
def group_data(request):
    groups=Group.objects.prefetch_related('permissions').all()
    return render(request,'admin/group_list.html',{'groups':groups})

class ProfileView(TemplateView):
    template_name="accounts/prfile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context["username"]=user.username
        context['email']=user.email
        context['name']=user.get_full_name()
        context["member_since"]=user.date_joined
        context["last_login"]=user.last_login

        return context


class CustomPasswordResetView(PasswordResetView):
    form_class=CustomPasswordResetForm
    template_name="registration/reset_pass.html"
    success_url = reverse_lazy('login')


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context["protocol"]= 'https' if self.request.is_secure() else 'http'
        context["domain"]=self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request,"a success mail sent.Please check your email")
        return super().form_valid(form)


class CustomPasswordRestConfirmView(PasswordResetConfirmView):
    form_class=CustomPasswordResetConfirmForm
    template_name="registration/reset_pass.html"
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        messages.success(self.request,"Password has been reseted successfully")
        return super().form_valid(form)

        
    
        
    






