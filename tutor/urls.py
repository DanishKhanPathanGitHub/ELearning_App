from django.urls import path, include
from . import views

urlpatterns = [
    path('classroom/add/', views.classroomAdd, name='classroomAdd'),
    path('classroom/', views.classroom, name='tutorclassroom'),
    path('classroom/<int:id>/delete/', views.classroom_delete, name='classroom_delete'),
    path('classroom/<int:id>/assignments/add/', views.assignments_add, name='assignments_add'),
    path('classroom/<int:id>/assignments/<int:asid>/', views.SpecificAssignment, name='tutorSpecificAssignment'),
    path('classroom/<int:id>/assignments/<int:asid>/delete/', views.SpecificAssignment_delete, name='SpecificAssignment_delete'),
    #path('classrroom/<int:id>/lectures/add/', views.lectures_add, name='lectures_add'),
    path('classrroom/<int:id>/lectures/<int:lid>/', views.SpecificLecture, name='tutorSpecificLecture'), 
    #path('classrroom/<int:id>/lectures/<int:lid>/delete/', views.SpecificLecture_delete, name='SpecificLecture_delete'),
    path('classroom/<int:id>/announcements/<int:anid>/', views.SpecificAnnouncement, name='tutorSpecificAnnouncement'),
    #path('classroom/<int:id>/announcements/<int:anid>/delete/', views.SpecificAnnouncement_delete, name='SpecificAnnouncement_delete'),
    path('classroom/<int:id>/manage_students/', views.manage_students, name='manage_students'),
    path('classroom/<int:id>/manage_students/<int:stid>/', views.student_profile_manage, name='student_profile_manage'),
    #path('classroom/<int:id>/manage_students/<int:stid>/delete/', views.student_profile_manage_delete, name='student_profile_manage_delete'),
 ]
 