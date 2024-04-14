from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, userProfile
from classroom.models import Classroom


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
