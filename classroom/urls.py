from django.urls import path, include
from . import views

urlpatterns = [
    path('classroom/<int:id>', views.classroom, name='classroom'),
    path('classroom/join/', views.classroomJoin, name='classroomJoin'),
    path('classroom/<int:id>/assignments/', views.assignments, name='assignments'),
    path('classroom/<int:id>/assignments/<int:asid>/', views.SpecificAssignment, name='SpecificAssignment'),
    path('classroom/<int:id>/assignments/<int:asid>/delete/', views.SubmissionDelete, name='SubmissionDelete'),
    path('classrroom/<int:id>/lectures/', views.lectures, name='lectures'),
    path('classrroom/<int:id>/lectures/<int:lid>/', views.SpecificLecture, name='SpecificLecture'), 
    path('classroom/<int:id>/announcements/', views.announcements, name='announcements'),
    path('classroom/<int:id>/announcements/<int:anid>/', views.SpecificAnnouncement, name='SpecificAnnouncement'),
    path('classroom/<int:id>/', include('chatbox.urls')),
    path('tutor/', include('tutor.urls')),
 ]
 