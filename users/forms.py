from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django import forms



class RegisterForm(UserCreationForm):


    class Meta:
        model=User
        fields=['username','first_name','last_name','password1','password2','email']

    def __init__(self, *args, **kwargs):
        super(UserCreationForm,self).__init__(*args, **kwargs)

        for fileldbname in ['username','password1','password2']:
             self.fields[fileldbname].help_text=None



class  CustomRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomRegistrationForm,self).__init__(*args, **kwargs)
        self.fields['username'].help_text=None
    
    password=forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)


    class Meta:
        model=User
        fields=['username','first_name','last_name','email']

    def clean(self):
        cleaned_data = super().clean()
        p1=cleaned_data.get('password')
        p2=cleaned_data.get('confirm_password')

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("password is not match")
        
        return cleaned_data
    


    def clean_email(self):
      
      email = self.cleaned_data.get('email')
      email_exists = User.objects.filter(email=email).exists()

      if email_exists:
        raise forms.ValidationError("Email already exists")

      return email


    

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

    



       
