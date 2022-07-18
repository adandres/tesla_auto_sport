from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .decorators import unauthenticated_user, allowed_users
from .models import Role, Bundle, UserInfo, Schedule
from .forms import CreateUserForm, UserInfoForm, RoleForm, BundleForm, ScheduleForm, UserRoleForm


# Create your views here.


def home(request):
    return render(request, 'accounts/dashboard.html')


def contact(request):
    return render(request, 'accounts/contact.html')


def prices(request):
    bundles = Bundle.objects.all()

    return render(request, 'accounts/prices.html', {'bundles': bundles})


@unauthenticated_user
def loginPage(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('single_profile', request.user.id)
        else:
            messages.info(request, 'Les identifiants ne correspondent pas à ceux que nous avons')

    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')



def usercreation(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user.id)
            role = Role.objects.get(id=request.POST['role'])
            userinfo = UserInfo.objects.create(user_id=user.id, role=role)
            user = form.cleaned_data.get('email')
            messages.success(request, 'Le compte a bien été créé pour: ' + user)

    context = {'form': form}
    return render(request, 'accounts/usercreation.html', context)


@login_required(login_url='login')
def showRole(request):
    roles = Role.objects.all()
    context = {'roles': roles}
    return render(request, 'accounts/show_role.html', context)


@login_required(login_url='login')
def createRole(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = RoleForm()
        context = {'form': form}
        return render(request, 'accounts/create_role.html', context)


@login_required(login_url='login')
def updateRole(request, pk):
    role = Role.objects.get(id=pk)
    form = RoleForm(instance=role)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        context = {'form': form}
        return render(request, 'accounts/create_role.html', context)

@login_required(login_url='login')
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    userinfo = UserInfo.objects.get(user_id=request.user.id)
    form = UserRoleForm(request.POST or None, initial={'user': user})
    if request.method == 'POST':
        if form.is_valid():
            try:
                userinfo = form.save()
            except:
                userinfo = UserInfo.objects.get(user_id=pk)
            userinfo.phone = request.POST['phone']
            userinfo.city = request.POST['city']
            userinfo.address = request.POST['address']
            userinfo.postal_code = request.POST['postal_code']
            userinfo.save()
            return redirect('admin_panel')
        else:
            context = {'form': form, 'user': user, 'userinfo': userinfo}
            return render(request, 'accounts/update_user.html', context)
    else:
        context = {'form': form, 'user': user, 'userinfo': userinfo}
        return render(request, 'accounts/update_user.html', context)


@login_required(login_url='login')
def deleteRole(request, pk):
    role = Role.objects.get(id=pk)
    if request.method == "POST":
        role.delete()
        return redirect('admin_panel')
    else:
        context = {'role': role}
        return render(request, 'accounts/delete_role.html', context)

@login_required(login_url='login')
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    if request.method == "POST":
        user.delete()
        return redirect('admin_panel')
    else:
        context = {'user': user}
        return render(request, 'accounts/delete_user.html', context)


@login_required(login_url='login')
def showBundle(request):
    bundles = Bundle.objects.get()
    context = {'bundles': bundles}
    return render(request, 'accounts/show_bundle.html', context)


@login_required(login_url='login')
def createBundle(request):
    if request.method == 'POST':
        form = BundleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = BundleForm()
        context = {'form': form}
        return render(request, 'accounts/create_bundle.html', context)


@login_required(login_url='login')
def updateBundle(request, pk):
    bundle = Bundle.objects.get(id=pk)
    form = BundleForm(instance=bundle)
    if request.method == 'POST':
        form = BundleForm(request.POST, instance=bundle)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        context = {'form': form}
        return render(request, 'accounts/create_bundle.html', context)


@login_required(login_url='login')
def deleteBundle(request, pk):
    bundle = Bundle.objects.get(id=pk)
    if request.method == "POST":
        bundle.delete()
        return redirect('admin_panel')
    else:
        context = {'Bundle': bundle}
        return render(request, 'accounts/delete_bundle.html', context)


@login_required(login_url='login')
def adminPanel(request):
    bundles = Bundle.objects.all()
    roles = Role.objects.all().order_by('id')[:5]
    users = get_user_model().objects.all()
    users_infos = UserInfo.objects.all()
    schedules = Schedule.objects.all()
    context = {'bundles': bundles, 'roles': roles, 'users': users, 'users_infos': users_infos,'schedules': schedules}
    return render(request, 'accounts/admin_panel.html', context)


@login_required(login_url='login')
def singleProfile(request, pk):
    admin = False
    user_info = UserInfo.objects.filter(user_id=request.user.id).first()
    group = user_info.role.name
    if group == 'Student':
        user = get_user_model().objects.get(id=request.user.id)
        schedule = Schedule.objects.filter(student_id=request.user.id).all()
    else:
        user = get_user_model().objects.get(id=pk)
        schedule = Schedule.objects.filter(student_id=pk).all()
    if group == 'Admin' or group == 'Secretary':
        admin = True
    context = {'user': user, 'user_info': user_info, 'admin': admin, 'schedule': schedule}
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def add_appointments(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        print("aaaaaaaaaa")
        print(form.data['instructor'])
        if form.is_valid():
            print('bbbbbbbb')
            form.save()
            if request.user.group == 'admin' or request.user.group == 'secretary':
                return redirect('admin_panel')
            else:
                return redirect('instructor_panel')
        else:
            context = {'form': form}
            return render(request, 'accounts/create_appointment.html', context)
    else:
        form = ScheduleForm()
        context = {'form': form}
        return render(request, 'accounts/create_appointment.html', context)
    context = {}
    return render(request, 'accounts/profile.html', context)

