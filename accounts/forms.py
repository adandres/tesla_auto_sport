from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Role, Bundle, UserInfo, Schedule

# Create your forms here.
from .models import Role, Bundle, UserInfo, Schedule

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmation mot de passe'}))
    role= forms.ChoiceField(choices=[(o.id, str(o)) for o in Role.objects.all()]
        )
        
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Pseudo'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nom'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
        }


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['phone', 'address', "postal_code", "city"]
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Téléphone'}),
            'address': forms.TextInput(attrs={'placeholder': 'Adresse'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Code postal'}),
            "city": forms.TextInput(attrs={'placeholder': 'Ville'}),
        }

class UserRoleForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['phone', 'address', "postal_code", "city", "user", "role"]
       
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Téléphone'}),
            'address': forms.TextInput(attrs={'placeholder': 'Adresse'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Code postal'}),
            "city": forms.TextInput(attrs={'placeholder': 'Ville'}),
        }



class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['name']


class BundleForm(ModelForm):
    class Meta:
        model = Bundle
        fields = '__all__'


class ScheduleForm(ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'date_start': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

