from classroom.models import Classroom
from django import forms
from .models import *
from classroom.models import Assignment

class ClassroomForm(forms.ModelForm):
    cover_pic = forms.ImageField(widget=forms.FileInput())
    class Meta:
        model = Classroom
        fields = ("name", "description", "cover_pic", "code", "password",)

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')
        password = cleaned_data.get('password')

        if code and password:
            try:
                Classroom.objects.get(code=code, password=password)
                raise forms.ValidationError("A classroom with this code and password already exists.")
            except Classroom.DoesNotExist:
                if len(code)<6:
                    raise forms.ValidationError("code must be minimum 6 character long")
                if len(password)<8:
                    raise forms.ValidationError("password must be minimum 6 character long")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the error message for the code field validator
        self.fields['code'].validators[0].message = "Code must be at least 6 characters long."
        # Override the error message for the password field validator
        self.fields['password'].validators[0].message = "Password must be at least 8 characters long."

class AssignmentUpdateForm(forms.ModelForm):
    due_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"type": "datetime-local"}))
    class Meta:
        model = Assignment
        fields = ("due_date","late_submission_allow",)
    
