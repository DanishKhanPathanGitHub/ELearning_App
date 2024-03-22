from django.shortcuts import render, redirect



# Create your views here.
def classroomAdd(request):
    return render(request, 'tutor/classroom_add.html')

def classroom(request):
    return render(request, 'tutor/classroom.html')

def classroom_delete(request, id):
    return redirect('home')

def assignments_add(request, id):
    return render(request, 'tutor/assignments_add.html')

def SpecificAssignment(request, id, asid):
    return render(request, 'tutor/tutorSpecificAssignment.html')

def SpecificAssignment_delete(request, id, asid):
    return redirect('assignments')

def SpecificLecture(request, id, lid):
    return render(request, 'tutor/tutorSpecificLecture.html')

def SpecificAnnouncement(request, id, anid):
    return render(request, 'tutor/tutorSpecificAnnouncement.html')

def manage_students(request, id):
    return render(request, 'tutor/manage.students.html')

def student_profile_manage(request, id, stid):
    return render(request, 'tutor/student_profile_manage.html')

