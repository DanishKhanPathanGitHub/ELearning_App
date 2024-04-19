from classroom.models import *
from django import forms
from .models import *
from .utils import *


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ("code", "password",)

class AssignmentForm(forms.ModelForm):
    assignment=forms.FileField(widget=forms.FileInput(attrs={"class":"btn-btn-info"}), validators=[file_validator])
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    class Meta:
        model = Assignment
        fields = ("assignment", "name", "description", "due_date", "late_submission_allow",)

class AssignmentSubmissionForm(forms.ModelForm):
    submitted_file=forms.FileField(widget=forms.FileInput(attrs={"class":"btn-btn-info"}), validators=[file_validator])
    class Meta:
        model = AssignmentSubmission
        fields = ("submitted_file",)

class AnnouncementForm(forms.ModelForm):
    file=forms.FileField(widget=forms.FileInput(attrs={"class":"btn-btn-info"}), validators=[combine_file_validator], required=False)
    class Meta:
        model = Announcement
        fields = ("title", "content", "file", "link",)

class PlaylistForm(forms.ModelForm):
    
    class Meta:
        model = Playlist
        fields = ("name",)
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter playlist name'})
        }

class VideoLectureForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        class_id = kwargs.pop('class_id', None)
        initial_playlist = kwargs.pop('initial_playlist', None)

        super(VideoLectureForm, self).__init__(*args, **kwargs)

        if class_id:
            self.fields['playlist'].queryset = Playlist.objects.filter(classroom__id=class_id)
            
        if initial_playlist:
            self.fields['playlist'].initial = initial_playlist
            
    notes=forms.FileField(widget=forms.FileInput(attrs={"class":"btn-btn-info"}), validators=[combine_file_validator], required=False)
    class Meta:
        model = VideoLecture
        fields = ("name","video_link","playlist","notes",)
