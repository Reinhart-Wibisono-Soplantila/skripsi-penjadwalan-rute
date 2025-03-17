from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .form import RegisterForm, LoginForm, ProfileForm, UpdateForm, MyPasswordChangeForm
from proweb.decorators import group_required
from proweb.mixins import AdminRequiredMixin

@group_required('Admin')
def index(request):
    userObject = User.objects.prefetch_related('groups').all()
    context={
        'UserObject' : userObject
    }
    return render(request, 'user/index.html', context)

@group_required('Admin')
def update(request, userId):
    userObject = get_object_or_404(User, id=userId)
    print(userObject.groups.all())
    passwordForm = MyPasswordChangeForm(user=userObject, data=request.POST)
    userForm_updated = UpdateForm(request.POST or None, instance=userObject)
    # userForm_updated['group'].initial =userObject.groups.all()  # Set initial value untuk grup yang dipilih
    error=None
    if(request.method == 'POST'):
        if 'updateUser' in request.POST:
            if userForm_updated.is_valid():
                userForm_updated.save()
                print(userForm_updated.cleaned_data)  # Debugging
                userObject.groups.clear()  # Hapus semua grup yang ada
                userObject.groups.add(userForm_updated.cleaned_data['group'])  # Gunakan 'group' di sini
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('app_user:index')
        elif 'changePassword' in request.POST:
            passwordForm = MyPasswordChangeForm(user=userObject, data=request.POST)
            if passwordForm.is_valid():
                user = passwordForm.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('app_user:index')
            else:
                print(passwordForm.errors)
    context={
        'pageHeader' : "User's Update",
        'update_form':userForm_updated,
        'passwordForm':passwordForm,
        'error':error
    }
    return render(request, 'user/edit.html', context)

def delete(request, userId):
    user = get_object_or_404(User, id=userId)
    user.delete()
    return redirect('app_user:index')

@group_required('Admin', 'Driver')
def profile(request):
    profileForm = ProfileForm(instance=request.user)
    error=None
    if request.method == 'POST':
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('app_user:profile')
        else:
           error = profileForm.errors
    context={
        'profileForm':profileForm,
        'error' : error
    }
    return render(request, 'user/profile.html', context)

class RegisterView(AdminRequiredMixin, View):
    def get(self, request):
        register_form = RegisterForm()
        context={
            'register_form' : register_form,
        }
        return render(request, 'user/register.html', context)
    
    def post(self, request):
        register_form = RegisterForm(request.POST or None)
        error={}
        print(request.POST)
        if register_form.is_valid() :
            user=register_form.save()
            group = register_form.cleaned_data['group']  # Ganti dengan nama grup yang sesuai
            user.groups.add(group)
            # Save group data and associate with user
            return redirect('app_user:index')
        else:
            print('failed')
            error=register_form.errors
        context={
            'register_form':register_form,
            'error':error
        }
        return render(request, 'user/register.html', context)
    
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        context = {
            'form':form
        }
        return render(request, 'user/login.html', context)
    
    def post(self, request):
        form = LoginForm(data = request.POST)        
        context = {
            'form':form
        }
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print('okee')
                user = form.get_user()
                login(request, user)
                return redirect('app_dashboard:home')
            else:
                messages.error(request, "You are not registered")
        else:
            messages.error(request, "Wrong Username or Wrong Password.")
        return render(request, 'user/login.html', context)