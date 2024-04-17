from django.urls import path, include
from . import views

urlpatterns = [
    path('tutorClassroom/<int:id>/', views.tutorClassroom, name='tutorClassroom'),
    path('tutorClassroom/<int:id>/student/<int:stid>/', views.ClassroomStudent, name='ClassroomStudent'),
    path('classroom/add/', views.classroomAdd, name='classroomAdd'),
    path('classroom/<int:id>/delete/', views.classroom_delete, name='classroom_delete'),
    path('classroom/<int:id>/assignments/add/', views.assignments_add, name='assignments_add'),
    path('classroom/<int:id>/assignments/<int:asid>/', views.SpecificAssignment, name='tutorSpecificAssignment'),
    path('classroom/<int:id>/assignments/<int:asid>/delete/', views.SpecificAssignment_delete, name='SpecificAssignment_delete'),
    path('classrroom/<int:id>/LecturePlaylist/<int:pid>/SpecificLecture/<int:lid>/', views.SpecificLecture, name='tutorSpecificLecture'), 
    path('classrroom/<int:id>/LecturePlaylist/<int:pid>/add_lecture/', views.LectureAdd, name='lecture_add'), 
    #path('classrroom/<int:id>/lectures/<int:lid>/delete/', views.SpecificLecture_delete, name='SpecificLecture_delete'),
    path('classroom/<int:id>/announcements/add/', views.announcements_add, name='announcements_add'),
    path('classroom/<int:id>/announcements/<int:anid>/', views.SpecificAnnouncement, name='tutorSpecificAnnouncement'),
 ]
 