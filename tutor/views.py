from django.shortcuts import render, redirect
from classroom.models import Classroom, Assignment, AssignmentSubmission, Announcement
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_student, check_role_tutor
from classroom.utils import check_classroom_participant
from .forms import *
from accounts.models import userProfile
from classroom.forms import AssignmentForm, AnnouncementForm
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def classroomAdd(request):
    if request.POST:
        class_form = ClassroomForm(request.POST, request.FILES)
        if class_form.is_valid():
            Class = class_form.save(commit=False)
            Class.tutor = userProfile.objects.get(user=request.user)
            Class.save()
            return redirect('home')
    else:
        class_form = ClassroomForm()
    context = {
        "class_form":class_form
    }
    return render(request, 'tutor/classroom_add.html', context)

def classroom_delete(request, id):
    return redirect('home')

@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def assignments_add(request, id):
    if check_classroom_participant(request.user, id):
        Class = Classroom.objects.get(id=id)       
        assignment_form = AssignmentForm()
        if request.POST:
            assignment_form = AssignmentForm(request.POST, request.FILES)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.classroom = Class
                assignment.save()
                messages.success(request, 'assignment added succesfully')
                return redirect(f'/classroom/{Class.id}/assignments')
            else:
                messages.error(request, 'There is error while uploading assignment')
        context = {
            "current_classroom_id":Class.id,
            "assignment_form":assignment_form,
        }
        return render(request, 'tutor/assignments_add.html', context)
    else:
        return render(request, '403.html')
    


@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def SpecificAssignment(request, id, asid):
    if check_classroom_participant(request.user, id):
        Class = Classroom.objects.get(id=id)
        assignment = Assignment.objects.get(id=asid)
        assignment_form = AssignmentUpdateForm(instance=assignment)

        class_students = Class.students.all()
        assignment_submissions = AssignmentSubmission.objects.filter(assignment=assignment)
        StudentsSubmissions = dict()
        
        for student in class_students:
            try:
                StudentsSubmissions[student] = assignment_submissions.get(student=student)
            except:
                StudentsSubmissions[student] = None
        
        if request.POST:
            assignment_form = AssignmentUpdateForm(request.POST, instance=assignment)
            if assignment_form.is_valid():
                assignment = assignment_form.save(commit=False)
                assignment.classroom = Class
                assignment.save()
                messages.success(request, 'assignment update succesfully')
                return redirect(f'/tutor/classroom/{Class.id}/assignments/{assignment.id}')
            else:
                print(assignment_form.errors)
                messages.error(request, 'There is error while updating assignment')
        if request.GET:
            student_id = request.GET.get('approval')
            student = userProfile.objects.get(id=student_id)
            assignment_submission = assignment_submissions.get(student=student)
            assignment_submission.is_approved=True
            assignment_submission.save()
            return redirect(f'/tutor/classroom/{Class.id}/assignments/{assignment.id}')
        context = {
            "assignment":assignment,
            "assignment_form":assignment_form,
            "current_classroom_id":Class.id,
            "StudentsSubmissions":StudentsSubmissions,
            "class_students":class_students,
        }
        return render(request, 'tutor/tutorSpecificAssignment.html', context)        
    else:
        return render(request, '403.html')

@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def SpecificAssignment_delete(request, id, asid):
    if check_classroom_participant(request.user, id):
        Class = Classroom.objects.get(id=id)
        assignment = Assignment.objects.get(id=asid)
        assignment.assignment.delete()
        submitted_assignments=AssignmentSubmission.objects.filter(assignment=assignment)
        for file in submitted_assignments:
            file.submitted_file.delete()
        assignment.delete()
        messages.success(request, 'Assignment Delted')
        return redirect(f'/classroom/{Class.id}/assignments/')

def SpecificLecture(request, id, lid):
    return render(request, 'tutor/tutorSpecificLecture.html')

@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def announcements_add(request, id):
    user = request.user
    if check_classroom_participant(user, id):
        Class = Classroom.objects.get(id=id)
        announcement_form = AnnouncementForm()
        if request.POST:
            announcement_form = AnnouncementForm(request.POST, request.FILES) 
            if announcement_form.is_valid():
                announcement = announcement_form.save(commit=False)
                announcement.classroom = Class
                announcement.save()
                messages.success(request, "announcement added succesfully")
                return redirect(f'/classroom/{Class.id}/announcements/')
            else:
                print(announcement_form.errors)
                messages.error(request, 'There is error while uploading announcement')
        context = {
            "announcement_form":announcement_form,
            "current_classroom_id":Class.id,    
        }
        return render(request, 'tutor/announcements_add.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def SpecificAnnouncement(request, id, anid):
    user = request.user
    Class = Classroom.objects.get(id=id)
    if check_classroom_participant(user, id):
        announcement = Announcement.objects.get(id=anid)
        if request.POST:
            try:
                announcement.file.delete()
                announcement.delete()
                return redirect(f'/classroom/{Class.id}/announcements/')
            except:
                announcement.delete()
                return redirect(f'/classroom/{Class.id}/announcements/')
        context = {
            "announcement":announcement,
            "current_classroom_id":Class.id,
            "anid":anid,
        }
        return render(request, 'tutor/tutorSpecificAnnouncement.html', context)
    

def manage_students(request, id):
    return render(request, 'tutor/manage.students.html')

def student_profile_manage(request, id, stid):
    return render(request, 'tutor/student_profile_manage.html')

