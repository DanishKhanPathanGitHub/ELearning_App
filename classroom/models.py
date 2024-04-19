from django.db import models
from accounts.models import User, userProfile
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


    class Meta:
        verbose_name = ("classroom")
        verbose_name_plural = ("classrooms")

    def __str__(self):
        return self.name
    
    def deactivate(self):
        return True
    
class StudentClassroom(models.Model):
    student = models.ForeignKey(userProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'classroom')

class Assignment(models.Model):
    name = models.CharField(max_length=50)
    assignment = models.FileField(upload_to='class/assignments', null=True, blank=False)
    classroom = models.ForeignKey(Classroom,  on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    due_date = models.DateTimeField(auto_now_add=False)
    description = models.TextField(null=True, blank=True)
    late_submission_allow = models.BooleanField(default=False)
    

    class Meta:
        verbose_name = ("Assignment")
        verbose_name_plural = ("Assignments")

    def __str__(self):
        return self.name

class AssignmentSubmission(models.Model):
    submitted_file = models.FileField(upload_to='class/assignments_submissions', null=True, blank=False)
    assignment = models.ForeignKey(Assignment,  on_delete=models.CASCADE)
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
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    read_status = models.ManyToManyField(userProfile, related_name='students_read')
    upload_date = models.DateTimeField(auto_now_add=True)
    link = models.URLField(max_length=1000, null=True, blank=True)
    tutor_link = models.URLField(max_length=1000, null=True, blank=True)
    class Meta:
        verbose_name = ("announcement")
        verbose_name_plural = ("announcements")

    def __str__(self):
        return self.title
    
class Playlist(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Playlist")
        verbose_name_plural = ("Playlists")

    def __str__(self):
        return self.name

class VideoLecture(models.Model):
    name = models.CharField(max_length=250)
    video_link = models.URLField(max_length=1000)
    notes = models.FileField(upload_to='class/LectureNotes', null=True, blank=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE) 
    upload_date = models.DateField(auto_now_add=True)
    class Meta:
        verbose_name = ("VideoLecture")
        verbose_name_plural = ("VideoLectures")
    
    def __str__(self):
        return self.name

    