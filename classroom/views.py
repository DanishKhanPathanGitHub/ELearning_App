from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.utils import check_role_student, check_role_tutor
from .utils import check_classroom_participant
import os
import datetime
from django.utils import timezone
from .models import *
from .forms import AssignmentSubmissionForm, PlaylistForm, VideoLectureForm, LectureNotesForm, VideoLectureUpdateForm
from accounts.models import userProfile, User
from django.contrib import messages
# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_role_student)
def classroom(request, id):
    user = request.user  # Access the authenticated user
    if check_classroom_participant(user, id):
        classroom = get_object_or_404(Classroom, id=id)
        context = {
            "classroom":classroom,
            "current_classroom_id": classroom.id,
        }
        return render(request, 'classroom/classroom.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_student)
def classroomJoin(request):
    if request.POST:
        code = request.POST['code']
        password = request.POST['password']
        try:
            classroom_to_join = Classroom.objects.get(code=code, password=password)
            user_profile = userProfile.objects.get(user=request.user)
            if classroom_to_join.students.filter(user=request.user).exists():
                messages.warning(request, 'You are already a member of this classroom.')
                return redirect('home')
            classroom_to_join.students.add(user_profile)
            StudentClassroom.objects.create(student=user_profile, classroom=classroom_to_join)
            messages.success(request, 'succesfully joined the class')
            return redirect('home')
        except:
            messages.error(request, 'invalid class credentials')
            return redirect('classroomJoin')
   
    return render(request, 'classroom/classroomJoin.html')

@login_required(login_url='login')
def assignments(request, id):
    user = request.user  # Access the authenticated user
    if check_classroom_participant(user, id):
        Class = Classroom.objects.get(id=id)                                        
        assignments = Assignment.objects.filter(classroom=Class)
        context = {
            "assignments":assignments,
            "current_classroom_id":Class.id,
        }
        return render(request, 'classroom/assignments.html', context)
    else:
        return render(request, '403.html')
    
@login_required(login_url='login')
@user_passes_test(check_role_student)    
def SpecificAssignment(request, id, asid):
    user = request.user
    assignment = Assignment.objects.get(id=asid)
    if check_classroom_participant(user, id):
        if assignment.classroom.id != id:
            return render(request, '404.html') 
        Class = Classroom.objects.get(id=id)                                   
        user_profile = userProfile.objects.get(user=user)
        try:
            check = AssignmentSubmission.objects.get(assignment=assignment, student=user_profile)
            submission_status = True
        except:
            check = None
            submission_status = False

        file_extension = os.path.splitext(assignment.assignment.name)[1].lower().strip('.')
        if request.POST:
            submission_form = AssignmentSubmissionForm(request.POST, request.FILES)
            if check:
                check.submitted_file.delete()
                check.delete()
            if submission_form.is_valid():
                submission = submission_form.save(commit=False)
                upload_date = timezone.make_aware(datetime.datetime.now())
                print(upload_date)
                print(assignment.due_date)
                if upload_date > assignment.due_date:
                    if assignment.late_submission_allow == True:
                        submission.assignment = assignment
                        submission.late_submission = True
                        submission.save()
                        submission.student.add(user_profile)
                        messages.warning(request, 'Late submission done!')
                        return redirect(f'/classroom/{Class.id}/assignments/{asid}')
                    else:
                        messages.warning(request, 'You are unable to submit assignment after due date passed')
                        return redirect(f'/classroom/{Class.id}/assignments/{asid}')
                else:
                    submission.assignment = assignment
                    submission.save()
                    submission.student.add(user_profile)
                    messages.success(request, 'Assignment submitted succesflly before due date')
                    return redirect(f'/classroom/{Class.id}/assignments/{asid}')
            else:
                messages.warning(request, 'There is error while submitting assignment')
                return redirect(f'/classroom/{Class.id}/assignments/{asid}')
        else:    
            submission_form = AssignmentSubmissionForm()

        context = {
            "assignment":assignment,
            "asid":asid,
            "current_classroom_id":Class.id,
            "file_extension":file_extension,
            "submission_form":submission_form,
            "submission_status":submission_status,
            "check":check,
        }
        return render(request, 'classroom/SpecificAssignment.html', context)
    else:
        return render(request, '403.html')

@login_required(login_url='login')
@user_passes_test(check_role_student) 
def SubmissionDelete(request, id, asid):
    user = request.user
    Class = Classroom.objects.get(id=id)
    if check_classroom_participant(user, id):                                
        assignment = Assignment.objects.get(id=asid)
        user_profile = userProfile.objects.get(user=user)
        try:
            check = AssignmentSubmission.objects.get(assignment=assignment, student=user_profile)
        except:
            check = None
        if check:
            check.submitted_file.delete()
            check.delete()
            messages.success(request, 'submission removed!')
            return redirect(f'/classroom/{Class.id}/assignments/{asid}')
        else:
            messages.error(request, 'No submission found')
            return redirect(f'/classroom/{Class.id}/assignments/{asid}')

@login_required(login_url='login')
def LecturePlaylists(request, id):
    Class = Classroom.objects.get(id=id)
    if check_classroom_participant(request.user, id):    
        playlists = Playlist.objects.filter(classroom=Class)  
        playlist_form = PlaylistForm()
        if request.GET:
            playlist_id = request.GET.get('playlist_id')
            playlist = Playlist.objects.get(id=playlist_id)
            playlist.delete()
            messages.success(request, 'playlist deleted')
            return redirect(f'/classroom/{Class.id}/LecturePlaylists')
        
        if request.POST:
            playlist_form = PlaylistForm(request.POST)
            if playlist_form.is_valid():
                playlist = playlist_form.save(commit=False)
                playlist.classroom = Class
                playlist.save()
                messages.success(request, 'Playlist added')
                return redirect(f'/classroom/{Class.id}/LecturePlaylists')
            else:
                messages.warning(request, 'Error while adding playlist')
                return redirect(f'/classroom/{Class.id}/LecturePlaylists')
        context = {
            "current_classroom_id":Class.id,
            "playlists":playlists,
            "playlist_form":playlist_form,
        }
        return render(request, 'classroom/LecturePlaylist.html', context)

@login_required(login_url='login')
def SpecificPlaylist(request, id, pid):
    Class = Classroom.objects.get(id=id)
    playlist = Playlist.objects.get(id=pid)
    if check_classroom_participant(request.user, id):
        if playlist.classroom != Class:
            return render(request, '404.html')
        lectures = VideoLecture.objects.filter(playlist=playlist)
        context = {
            "playlist":playlist,
            "lectures":lectures,
            "current_classroom_id":Class.id,
            "pid":pid,
        }
        return render(request, 'classroom/SpecificPlaylist.html', context)

@login_required(login_url='login')
def SpecificLecture(request, id, pid, lid):
    Class = Classroom.objects.get(id=id)
    playlist = Playlist.objects.get(id=pid)
    lecture = VideoLecture.objects.get(id=lid)
    if check_classroom_participant(request.user, id):
        if playlist.classroom != Class or lecture.playlist != playlist:
            return render(request, '404.html')
        lecture_notes_form = LectureNotesForm()
        lecture_update_form = VideoLectureForm(instance=lecture)
        notes = LectureNote.objects.filter(video_lecture= lecture)
        if request.POST:
            if notes.count()>=3:
                messages.warning(request, 'one lecture cannot have more than 3 notes')
                return redirect(f'/classroom/{id}/LecturePlaylists/{pid}/Lecture/{lid}')
            lecture_notes_form = LectureNotesForm(request.POST, request.FILES)
            if lecture_notes_form.is_valid():
                lecture_form = lecture_notes_form.save(commit=False)
                lecture_form.video_lecture = lecture
                lecture_form.save()
                messages.success(request, 'Notes added succesfully')
                return redirect(f'/classroom/{id}/LecturePlaylists/{pid}/Lecture/{lid}')
        context = {
            "current_classroom_id":Class.id,
            "playlist":playlist,
            "lecture":lecture,
            "lecture_notes_form":lecture_notes_form,
            "notes":notes,
            "lecture_update_form":lecture_update_form,
        }
        return render(request, 'classroom/SpecificLecture.html', context)
    
@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def SpecificLectureDelete(request, id, pid, lid):
    Class = Classroom.objects.get(id=id)
    if check_classroom_participant(request.user, id):
        playlist = Playlist.objects.get(id=pid)
        lecture = VideoLecture.objects.get(id=lid)
        notes = LectureNote.objects.filter(video_lecture=lecture)
        if request.GET:
            lecture.delete()
            messages.success(request, 'lecture deleted succesfully')
            return redirect(f'/classroom/{id}/LecturePlaylists/{pid}/')

@login_required(login_url='login')
@user_passes_test(check_role_tutor)
def SpecificLectureUpdate(request, id, pid, lid):
    Class = Classroom.objects.get(id=id)
    if check_classroom_participant(request.user, id):
        lecture = VideoLecture.objects.get(id=lid)
        playlist = request.POST['playlist']
        lecture.playlist = Playlist.objects.get(id=playlist)
        
        lecture.save()
        messages.success(request, 'playlist updated')
        return redirect(f'/classroom/{id}/LecturePlaylists/{lecture.playlist.id}/')

@login_required(login_url='login')
def announcements(request, id):
    user = request.user
    if check_classroom_participant(user, id): 
        Class = Classroom.objects.get(id=id)
        user_profile = userProfile.objects.get(user=user)
        announcements = Announcement.objects.filter(classroom=Class).order_by('-upload_date')
        unread_announcemnets = []
        filter = request.GET.get('filter', 'latest')
        for announcement in announcements:
            if user_profile in announcement.read_status.all():
                print(user_profile, ' in ', announcement )
                pass
            else:
                print(user_profile, ' not in ', announcement )
                unread_announcemnets.append(announcement)
        context = {
            "announcements":announcements,
            "unread_announcemnets":unread_announcemnets,
            "current_classroom_id":Class.id,
            "filter":filter,
        }
        return render(request, 'classroom/announcements.html', context)

@login_required(login_url='login')
@user_passes_test(check_role_student) 
def SpecificAnnouncement(request, id, anid):
    user = request.user
    Class = Classroom.objects.get(id=id)
    announcement = Announcement.objects.get(id=anid)
    if check_classroom_participant(user, id):
        if announcement.classroom != Class:
            return render(request, '404.html')
        
        user_profile = userProfile.objects.get(user=user)
        announcement.read_status.add(user_profile)
        context = {
            "announcement":announcement,
            "current_classroom_id":Class.id,
            "anid":anid,
        }
        return render(request, 'classroom/SpecificAnnouncement.html', context)

