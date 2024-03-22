from django.shortcuts import render

# Create your views here.

def classroom(request):
    return render(request, 'classroom/classroom.html')

def assignments(request, id):
    return render(request, 'classroom/assignments.html')

def SpecificAssignment(request, id, asid):
    return render(request, 'classroom/SpecificAssignment.html')

def lectures(request, id):
    return render(request, 'classroom/lectures.html')

def SpecificLecture(request, id, lid):
    return render(request, 'classroom/SpecificLecture.html')

def announcements(request, id):
    return render(request, 'classroom/announcements.html')

def SpecificAnnouncement(request, id, anid):
    return render(request, 'classroom/SpecificAnnouncement.html')

