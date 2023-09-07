from django import views
from .models import UserDetail
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserDetailForm, UserForm, LoginForm , UpdateUserForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django import views
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout

# Create your views here.


class MyRegister(views.View):
    template_name = "register.html"
    user_form = UserForm
    user_detail_form = UserDetailForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            form1 = self.user_form()
            form2 = self.user_detail_form()
            return render(request, self.template_name, {"form1": form1, "form2": form2})

    def post(self, request):

        user_form = self.user_form(request.POST, request.FILES)
        user_detail_form = self.user_detail_form(request.POST, request.FILES)
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            if user_form.is_valid() and user_detail_form.is_valid():
                username = user_form.cleaned_data['username']
                first_name = user_form.cleaned_data['first_name']
                last_name = user_form.cleaned_data['last_name']
                password1 = user_form.cleaned_data['password']
                password2 = user_form.cleaned_data['password2']
                email = user_form.cleaned_data['email']
                mobile = user_detail_form.cleaned_data['mobile']

                if password1 != password2:
                    user_form.add_error("__all__", 'Passwords not matching')
                elif User.objects.filter(email=email).exists():
                    user_form.add_error("email", 'Email Address Taken')
                else:
                    current_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                            password=password1, email=email)
                    current_user_detail = user_detail_form.save(commit=False)
                    current_user_detail.user = current_user
                    current_user_detail.save()
                    login(request, current_user)
                    return redirect('/home/')
                return render(request, self.template_name, {'form1': user_form, 'form2': user_detail_form})
            else:
                return render(request, self.template_name, {'form1': user_form, 'form2': user_detail_form})


class MyLogin(views.View):
    template_name = "login.html"
    form_class = LoginForm

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            form = self.form_class(request.POST or None)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                current_user = authenticate(
                    request, username=username, password=password)
                # print(type(current_user))
                if current_user is None:
                    form.add_error("__all__", 'Invalid username or password')
                    return render(request, self.template_name, {"form": form})
                else:
                    login(request, current_user)
                    return redirect('/home/')
            else:
                return render(request, self.template_name, {"form": form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            form = self.form_class()
            print("hello from my login get")
            return render(request, "login.html", {"form": form})


def my_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    else:
        return redirect('/')


# messages.info(request, '4')
# return HttpResponse('hi') replaces current html content
# render(request, 'base.html', {'a': b} process base with the json data


class ShowProfileDetail(views.View):
    def get(self, request, user_id):
        user_detail = UserDetail.objects.get(pk=user_id)
        user = User.objects.get(userdetail=user_detail)
        return render(request, "profile.html", {'user': user, 'user_detail': user_detail})




def index(request):
    return render(request, 'index.html')

def host(request):
    return render(request, 'host.html')

def home(request):
    return render(request, 'home.html')


class Profile(views.View):
    template_name = 'profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get(user=request.user)
            context = {'user': request.user, 'user_detail': user_detail}
            return render(request, self.template_name, context)
        else:
            messages.info(request, 'Log in first')
            return redirect('/')


def edit_profile(request):
    if request.user.is_authenticated:
        user = request.user
        user_detail = UserDetail.objects.get(user=user)

        if request.method == 'GET':
            user_form = UpdateUserForm(instance=user)
            user_detail_form = UserDetailForm(instance=user_detail)
            context = {
                'user_form': user_form, 'user_detail_form': user_detail_form
            }
            return render(request, 'edit_profile.html', context)

        else:
            print("edit profile post")
            user_form = UpdateUserForm(
                request.POST, request.FILES, instance=user)
            user_detail_form = UserDetailForm(
                request.POST, request.FILES, instance=user_detail)
            if user_form.is_valid() and user_detail_form.is_valid():
                user_form.save()
                user_detail_form.save()
                messages.info(request, 'Successfully updated')
                return redirect('/profile/')
            else:
                context = {
                    'user_form': user_form, 'user_detail_form': user_detail_form
                }
                return render(request, 'edit_profile.html', context)

    else:
        messages.info(request, 'Log in first')
        return redirect('/')


class ChangePassword(views.View):
    template_name = 'change_password.html'
    form_class = PasswordChangeForm

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/')

    def post(self, request):

        if request.user.is_authenticated:
            user = request.user
            form = self.form_class(request.POST or None)

            if form.is_valid():
                username = user.username
                password = form.cleaned_data['current_password']
                new_pass = form.cleaned_data['new_password']
                confirm_pass = form.cleaned_data['confirm_password']
                auth_user = authenticate(
                    request, username=username, password=password)
                if auth_user is not None:
                    if new_pass == confirm_pass:
                        auth_user.set_password(new_pass)
                        print('cppost')
                        auth_user.save()
                        login(request, auth_user)
                        return redirect('/home/')
                    else:
                        messages.info(request, 'Passwords not matching')
                        return redirect('/change_password/')
                else:
                    messages.info(request, 'Permission denied')
                    return redirect('/underground/')
            else:
                return render(request, self.template_name, {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/')


class Underground(views.View):
    template_name = 'underground.html'

    def get(self, request):
        return render(request, self.template_name)


class PermissionDenied(views.View):

    def get(self, request):
        messages.info(request, 'Permission Denied')
        return redirect('/')
    
    
class MyOrder(views.View):
    template_name = "my_order.html"
    
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
