from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, userProfile
from accounts.forms import userProfileForm, userMiniForm
from classroom.models import Classroom
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    try:
        user_profile = userProfile.objects.get(user=request.user)
        if user_profile.user.role == 1:
            print('classroom check')
            classrooms = Classroom.objects.filter(students=user_profile)
        else:
            classrooms = Classroom.objects.filter(tutor=user_profile)
    except:
        classrooms=None
        user_profile=None

    context = {
        "classrooms":classrooms,
        "user_profile":user_profile,
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def profile(request):
    user_profile = userProfile.objects.get(user=request.user)
    user_profile_form = userProfileForm(instance=user_profile)
    user_mini_form = userMiniForm(instance=user_profile.user)
    if request.POST:
        print('inside post update')
        user_profile_form = userProfileForm(request.POST, request.FILES, instance=user_profile)
        user_mini_form = userMiniForm(request.POST, instance=request.user)
        if user_profile_form.is_valid() and user_mini_form.is_valid():
            print('valid forms')
            user_mini = user_mini_form.save()
            
            user_profile = user_profile_form.save(commit=False)
            user_profile.user = user_mini  # Assuming request.user is the current logged-in user
            user_profile.save()
            messages.success(request, "user data updated")
            return redirect('/profile')
        else:
            print('invalid forms')
            
    context = {
        "user_profile":user_profile,
        "user_profile_form":user_profile_form,
        "user_mini_form":user_mini_form,
    }
    return render(request, 'profile.html', context)

