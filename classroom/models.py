from typing import Any
from django.db import models
from accounts.models import User, userProfile
from embed_video.fields import EmbedVideoField
from django.core.validators import MinLengthValidator, MaxLengthValidator
# Create your models here.

class Classroom(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    tutor = models.ForeignKey(userProfile, on_delete=models.CASCADE, related_name='classroom_tutor')
    students = models.ManyToManyField(userProfile, related_name='classroom_students', blank=True)
    cover_pic = models.ImageField(upload_to='class_coverpics', blank=True, null=True)
    code = models.CharField(MinLengthValidator(6), max_length=10, unique=True)
    password = models.CharField(MinLengthValidator(8), max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        # Delete related Assignments -> assignment submission and his related files will be deleted automatically
        for assignment in self.assignments.all():
            assignment.delete()
        #delete related playlist -> related lectures and associated files will be delete automatically
        for playlist in self.playlists.all():
            playlist.delete()
        #delete related Announcements -> related files will be deleted automatically
        for announcement in self.announcements.all():
            announcement.delete()
        
        for student_data in self.classroom_students_data.all():
            student_data.delete()
        
        self.cover_pic.delete()
        super().delete(*args, **kwargs)



    class Meta:
        verbose_name = ("classroom")
        verbose_name_plural = ("classrooms")

    def __str__(self):
        return self.name
    
    
class StudentClassroom(models.Model):
    student = models.ForeignKey(userProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, related_name='classroom_students_data', on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'classroom')

class Assignment(models.Model):
    name = models.CharField(max_length=50)
    assignment = models.FileField(upload_to='class/assignments', null=True, blank=False)
    classroom = models.ForeignKey(Classroom, related_name='assignments', on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now_add=False)
    description = models.TextField(null=True, blank=True)
    late_submission_allow = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = ("Assignment")
        verbose_name_plural = ("Assignments")

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete related LectureNotes
        for submissiom in self.assignment_submissions.all():
            submissiom.submitted_file.delete()
            submissiom.delete()

        # Delete related Announcement
        link = f'/classroom/{self.classroom.id}/assignments/{self.id}/'
        try:
            announcement = Announcement.objects.get(link=link)
            announcement.delete()
        except Announcement.DoesNotExist:
            pass
        self.assignment.delete()
        super().delete(*args, **kwargs)

class AssignmentSubmission(models.Model):
    submitted_file = models.FileField(upload_to='class/assignments_submissions', null=True, blank=False)
    assignment = models.ForeignKey(Assignment,  related_name='assignment_submissions', on_delete=models.CASCADE)
    upload_date = models.DateField(auto_now_add=True)
    student = models.ManyToManyField(userProfile, related_name='students_submissions')
    late_submission = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    class Meta:
        verbose_name = ("AssignmentSubmissions")
        verbose_name_plural = ("AssignmentsSubmissions")


class Announcement(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='class/announcements',null=True, blank=True)
    content = models.TextField()
    classroom = models.ForeignKey(Classroom, related_name='announcements', on_delete=models.CASCADE)
    read_status = models.ManyToManyField(userProfile, related_name='students_read')
    upload_date = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=1000, null=True, blank=True)
    tutor_link = models.URLField(max_length=1000, null=True, blank=True)
    class Meta:
        verbose_name = ("announcement")
        verbose_name_plural = ("announcements")

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        # Delelete announcements files if exist
        if self.file:
            self.file.delete()
        super().delete(*args, **kwargs)

class Playlist(models.Model):
    classroom = models.ForeignKey(Classroom, related_name='playlists', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Playlist")
        verbose_name_plural = ("Playlists")

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        for lecture in self.video_lectures.all():
            lecture.delete()
        
        super().delete(*args, **kwargs)

class VideoLecture(models.Model):
    name = models.CharField(max_length=250)
    video_link = EmbedVideoField()
    playlist = models.ForeignKey(Playlist, related_name='video_lectures', on_delete=models.CASCADE) 
    upload_date = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = ("VideoLecture")
        verbose_name_plural = ("VideoLectures")
    
    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete related LectureNotes
        for note in self.lecture_notes.all():
            note.note_file.delete()
            note.delete()

        # Delete related Announcement
        link = f'/classroom/{self.playlist.classroom.id}/LecturePlaylists/{self.playlist.id}/Lecture/{self.id}/'
        try:
            announcement = Announcement.objects.get(link=link)
            announcement.delete()
        except Announcement.DoesNotExist:
            pass

        super().delete(*args, **kwargs)

class LectureNote(models.Model):
    video_lecture = models.ForeignKey(VideoLecture, related_name='lecture_notes', on_delete=models.CASCADE)
    note_file = models.FileField(upload_to='class/LectureNotes')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lecture Note"
        verbose_name_plural = "Lecture Notes"

    def __str__(self):
        return f"Lecture Note for {self.video_lecture.name}"