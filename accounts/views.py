
from django import views
from django.contrib import messages, auth
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User, auth
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django import views
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from .forms import CreateUserForm, LoginForm, PasswordChangeForm
from .models import UserDetail, City, Country
from django.contrib.auth.hashers import make_password, check_password



class MyHome(views.View):
    template_name = "home.html"

    def get(self, request):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        else:
            return redirect('/accounts/login/')


class MyRegister(views.View):
    template_name = "register.html"
    form_temp = CreateUserForm

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/accounts/home/')
        else:
            form = self.form_temp()
            print("hello from my register get")
            return render(request, "register.html", { "form": form })

    def post(self, request):

        
        form = self.form_temp(request.POST, request.FILES)
        if request.user.is_authenticated:
            return redirect('/accounts/home/')
        else:
            if form.is_valid() :
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']
                mail = form.cleaned_data['mail']
                mobile = form.cleaned_data['mobile']
                nid = form.cleaned_data['nid']

                if password != confirm_password:
                    form.add_error("__all__", 'Passwords not matching')
                elif UserDetail.objects.filter(mail=mail).exists():
                    form.add_error("mail", 'Email Address Taken')
                elif UserDetail.objects.filter(username=username).exists():
                    form.add_error("username", 'Username Taken')
                elif UserDetail.objects.filter(mobile=mobile).exists():
                    form.add_error("mobile", 'Mobile Numbet Taken')
                elif UserDetail.objects.filter(nid=nid).exists():
                    form.add_error("nid", 'NID already taken')
                else:
                    current_user_detail = form.save(commit=False)
                    current_user_detail.password = make_password( password )
                    try:
                        current_user_detail.save()
                        login(request, current_user_detail )
                        return redirect('/accounts/home/')
                    except ValidationError as e:
                        for k in e:
                            form.add_error(k, e[k])
                        return render(request, self.template_name, {'form': form })
                
                return render(request, self.template_name, {'form': form })
            else:
                return render(request, self.template_name, {'form': form })
            


class MyProfile(views.View):
    template_name = 'profile.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get( username=request.user.username )
            context = {'user_detail': user_detail}
            return render(request, self.template_name, context)
        else:
            messages.info(request, 'Log in first')
            return redirect('/accounts/')
        
    def post(self, request):
        if request.user.is_authenticated:
            user_detail = UserDetail.objects.get( username=request.user.username )
            context = {'user_detail': user_detail}
            return render(request, self.template_name, context)
        else:
            messages.info(request, 'Log in first')
            return redirect('/accounts/')


class MyLogin(views.View):
    template_name = "login.html"
    form_class = LoginForm

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/accounts/home/')
        else:
            form = self.form_class(request.POST or None)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                current_user = authenticate(request, username=username, password=password)
                # print(type(current_user))
                if current_user is None:
                    form.add_error("__all__", 'Invalid username or password')
                    return render(request, self.template_name, {"form": form})
                else:
                    login(request, current_user)
                    return redirect('/accounts/home/')
            else:
                return render(request, self.template_name, {"form": form})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/accounts/home/')
        else:
            form = self.form_class()
            print("hello from my login get")
            return render(request, "login.html", {"form": form})
        
class ForgotPassword(views.View):
    
    def get(self, request):
        return render(request, 'forgot_password.html')
    
    def post(self, request):
        aha=0


class MyLogout(views.View):
        
        def get(self, request):

            if request.user.is_authenticated:
                logout(request)
                return redirect('/accounts/')
            else:
                return redirect('/accounts/')
            

class ShowProfileDetail(views.View):
    def get(self, request, user_id):
        user_detail = UserDetail.objects.get(pk=user_id)
        return render(request, "profile.html", { 'user_detail': user_detail})



############################ update profile ############################

from .forms import UpdateMobileForm, UpdateMailForm, UpdateNameForm


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
            return redirect('/accounts/')

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


from .forms import UpdateNameForm

class UpdateName(views.View):
    

    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateNameForm()
            return render(request, 'update_name.html', {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
    
    def post(self, request):

        if request.user.is_authenticated:
            form = UpdateNameForm(request.POST or None)
            
            if form.is_valid():
                name = form.cleaned_data['name']
                user_detail = UserDetail.objects.get(username=request.user.username)
                user_detail.name = name
                user_detail.save()
                return redirect( "/accounts/my_profile/" )
            else:
                return render(request, 'update_name.html', {'form': form})
            
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
        
from .forms import UpdateMailForm

class UpdateEmail(views.View):
    

    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateMailForm()
            return render(request, 'update_mail.html', {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
    
    def post(self, request):

        if request.user.is_authenticated:
            form = UpdateNameForm(request.POST or None)
            
            if form.is_valid():
                mail = form.cleaned_data['mail']
                user_detail = UserDetail.objects.get(username=request.user.username)
                user_detail.mail = mail
                try:
                    user_detail.save()
                    return redirect( "/accounts/my_profile/" )
                except:
                    form.add_error('mail', 'Email Address Taken')
                    return render(request, 'update_mail.html', {'form': form})
            else:
                return render(request, 'update_name.html', {'form': form})
            
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')

from .forms import UpdateMobileForm



class UpdateMobile(views.View):
    
    def get(self, request):
        if request.user.is_authenticated:
            form = UpdateMobileForm()
            return render(request, 'update_mobile.html', {'form': form})
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')
    
    def post(self, request):

        if request.user.is_authenticated:
            form = UpdateMobileForm(request.POST or None)
            
            if form.is_valid():
                mobile = form.cleaned_data['mobile']
                user_detail = UserDetail.objects.get(username=request.user.username)
                user_detail.mobile = mobile
                try:
                    user_detail.save()
                    return redirect( "/accounts/my_profile/" )
                except:
                    form.add_error('mobile', 'Mobile Number Taken')
                    return render(request, 'update_mobile.html', {'form': form})
            else:
                return render(request, 'update_mobile.html', {'form': form})
            
        else:
            messages.info(request, 'You must log in first')
            return redirect('/accounts/')




###################################### Orders ######################################




