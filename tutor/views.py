from django.shortcuts import render, redirect
from classroom.models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_tutor
from classroom.utils import check_classroom_participant
from .forms import *
from accounts.models import userProfile
from classroom.forms import AssignmentForm, AnnouncementForm, VideoLectureForm
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def tutorClassroom(request, id):
    user = request.user  # Access the authenticated user
    if check_classroom_participant(user, id):
        Class = Classroom.objects.get(id=id)  
        class_students = Class.students.all()
        context = {
            "Class":Class,
            "current_classroom_id": Class.id,
            "class_students":class_students,
        }
        return render(request, 'tutor/tutorClassroom.html', context)
    
@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def tutorClassroomDelete(request, id):
    user = request.user  # Access the authenticated user
    if check_classroom_participant(user, id):
        Class = Classroom.objects.get(id=id)  
        Class.delete()
        return redirect('/')

@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def ClassroomStudent(request, id, stid):
    if check_classroom_participant(request.user, id):
        Class = Classroom.objects.get(id=id)    
        student = userProfile.objects.get(id=stid)
        joined_date = StudentClassroom.objects.get(classroom=Class, student=student).joined_date
        if request.GET:
            try:
                for assignment in Assignment.objects.filter(classroom=Class):
                    submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)
                    submission.submitted_file.delete()
                    submission.delete()
            except:
                pass
            try:
                for announcement in Announcement.objects.filter(classroom=Class):
                    announcement.read_status.remove(student)
            except:
                pass
            StudentClassroom.objects.get(student=student, classroom=Class).delete()
            Class.students.remove(student)
            return redirect(f'/tutor/tutorClassroom/{Class.id}/')
        context = {
            "Class":Class,
            "current_classroom_id": Class.id,
            "student":student,
            "joined_date":joined_date,
        }
        return render(request, 'tutor/ClassroomStudent.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def classroomAdd(request):
    if request.POST:
        class_form = ClassroomForm(request.POST, request.FILES)
        if class_form.is_valid():
            Class = class_form.save(commit=False)
            Class.tutor = userProfile.objects.get(user=request.user)
            Class.save()
            messages.success(request, "class created succesfully")
            return redirect('home')
        else:
            messages.warning(request, "error while adding class")
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
    Class = Classroom.objects.get(id=id)
    assignment = Assignment.objects.get(id=asid)
    if check_classroom_participant(request.user, id):
        if assignment.classroom != Class:
            return render(request, '404.html')
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
        assignment.delete()
        messages.success(request, 'Assignment Delted')
        return redirect(f'/classroom/{Class.id}/assignments/')

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
    announcement = Announcement.objects.get(id=anid)
    if check_classroom_participant(user, id):
        if announcement.classroom != Class:
            return render(request, '404.html')
        if request.POST:
            announcement.delete()
            return redirect(f'/classroom/{Class.id}/announcements/')
        context = {
            "announcement":announcement,
            "current_classroom_id":Class.id,
            "anid":anid,
        }
        return render(request, 'tutor/tutorSpecificAnnouncement.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_tutor)   
def LectureAdd(request, id, pid):
     Class = Classroom.objects.get(id=id)
     if check_classroom_participant(request.user, id):
        try:
            playlist = Playlist.objects.get(id=pid)
        except:
            playlist = None
        video_lecture_form = VideoLectureForm(initial_playlist=playlist, class_id=id)
        if request.POST:
            video_lecture_form = VideoLectureForm(request.POST, class_id=id)
            if video_lecture_form.is_valid():
                video_lecture = video_lecture_form.save()
                messages.success(request, f'Lecture Added to {video_lecture.playlist.id} successfully!')
                return redirect(f'/classroom/{Class.id}/LecturePlaylists/{video_lecture.playlist.id}')
            else:
                messages.error(request, 'There is error while uploading video lecture')
        context = {
            "current_classroom_id":Class.id,
            "pid":pid,
            "video_lecture_form":video_lecture_form,
            "playlist":playlist,
        }
        return render(request, 'tutor/lecture_add.html', context)         


