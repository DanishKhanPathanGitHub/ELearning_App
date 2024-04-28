from django.urls import path, include
from . import views

urlpatterns = [
    path('classroom/<int:id>', views.classroom, name='classroom'),
    path('classroom/join/', views.classroomJoin, name='classroomJoin'),
    path('classroom/<int:id>/assignments/', views.assignments, name='assignments'),
    path('classroom/<int:id>/assignments/<int:asid>/', views.SpecificAssignment, name='SpecificAssignment'),
    path('classroom/<int:id>/assignments/<int:asid>/delete/', views.SubmissionDelete, name='SubmissionDelete'),
    path('classroom/<int:id>/LecturePlaylists/', views.LecturePlaylists, name='LecturePlaylists'),
    path('classroom/<int:id>/LecturePlaylists/<int:pid>/', views.SpecificPlaylist, name='SpecificPlaylist'),
    path('classroom/<int:id>/LecturePlaylists/<int:pid>/Lecture/<int:lid>/', views.SpecificLecture, name='SpecificLecture'), 
    path('classroom/<int:id>/LecturePlaylists/<int:pid>/Lecture/<int:lid>/delete/', views.SpecificLectureDelete, name='SpecificLectureDelete'), 
    path('classroom/<int:id>/LecturePlaylists/<int:pid>/Lecture/<int:lid>/update/', views.SpecificLectureUpdate, name='SpecificLectureUpdate'), 
    path('classroom/<int:id>/announcements/', views.announcements, name='announcements'),
    path('classroom/<int:id>/announcements/<int:anid>/', views.SpecificAnnouncement, name='SpecificAnnouncement'),
    path('classroom/<int:id>/', include('chatbox.urls')),
    path('tutor/', include('tutor.urls')),
 ]
 