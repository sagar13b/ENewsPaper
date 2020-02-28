from django.shortcuts import render, redirect
from .models import User, EditorProfile
#from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def surfer_signup(request):
    if request.method == 'POST':
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request, 'account/surfer_signup.html',{'error':'Email already exists'})
            except User.DoesNotExist:
                user = User.objects.create_user(email=request.POST['email'],password=request.POST['pass1'],fname = request.POST['fname'],lname = request.POST['lname'])
                if request.POST['mname'] is not None:
                    user.mname = request.POST['mname']
                    user.save()
                return render(request, 'account/signup_success.html')
        else:
            return render(request, 'account/surfer_signup.html',{'error':'Password did not match'})
    else:
        return render(request, 'account/surfer_signup.html')

def editor_signup(request):
    if request.method == 'POST':
        if request.POST['pass1'] == request.POST['pass2']:
            try:
                user = User.objects.get(email=request.POST['email'])
                return render(request, 'account/surfer_signup.html',{'error':'Email already exists'})
            except User.DoesNotExist:
                user = User.objects.create_editor(email=request.POST['email'],password=request.POST['pass1'],fname = request.POST['fname'],lname = request.POST['lname'])
                if request.POST['mname'] is not None:
                    user.mname = request.POST['mname']
                    user.save()
                e = EditorProfile()
                e.address = request.POST['address']
                e.phone_no = request.POST['phone_no']
                e.user_detail = user
                try:
                    e.profile_pic = request.FILES['ppic']
                    e.save()
                except:
                    e.save()
                return render(request, 'account/signup_success.html')
        else:
            return render(request, 'account/surfer_signup.html',{'error':'Password did not match'})
    else:
        return render(request, 'account/editor_signup.html')

def user_signin(request):
    if request.method == 'POST':
        user = auth.authenticate(email=request.POST['email'],password=request.POST['pass1'])
        if user is not None:
            auth.login(request, user)
            if user.is_admin:
                return redirect('ahome')
            elif user.is_editor:
                return redirect('ehome')
            elif user.is_surfer:
                return redirect('shome')
        else:
            try:
                user = User.objects.get(email=request.POST['email'])
                if user.active:
                    return render(request, 'account/signin.html', {'error': 'Password incorrect'})
                else:
                    return render(request, 'account/signin.html', {'error': 'Account is deactivated'})
            except User.DoesNotExist:
                return render(request, 'account/signin.html',{'error':'Email did not match'})
    else:
        return render(request, 'account/signin.html')

def user_signout(request):
    auth.logout(request)
    return redirect('shome')