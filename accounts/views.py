from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
def registerUser(request):
    return render(request, 'accounts/registerUser.html')

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return render('login')

def studentProfile(request):
    return render(request, 'accounts/studentProfile.html')

def tutorProfile(request):
    return render(request, 'accounts/tutorProfile.html')

def activate(request, uidb64, token):
    return redirect('Profile')

@login_required(login_url='login')    
def myAccount(request):
    redirecturl = '/'
    user = request.user
    print(user.role)
    if user.role == 2:
        redirecturl = 'tutorclassroom'
    elif user.role == 1:
        redirecturl = 'classroom'
        print('redirect url is :', redirecturl )
    elif user.role and user.is_active == True:
        redirecturl = 'admin/'
    
    return redirect(redirecturl)

def reset_password(request):
    return render(request, 'accounts/reset_password.html')

def reset_password_validate(request, uidb64, token):
    return redirect('reset_password')

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html') 