from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from classroom.models import Announcement, Assignment, AssignmentSubmission, VideoLecture, Classroom
@receiver(post_save, sender=Assignment)
#reciever will get the signal->post_save from sender-> user
#reciever function below will create/update the userProfile accordingly
#immediately after creation/updation of user(sender)
def assignment_post_save(sender, created, instance, **kwargs):
    if created:
        assignment = instance
        classroom = assignment.classroom
        
        link = f'/classroom/{classroom.id}/assignments/{assignment.id}/'
        tutor_link = f'/tutor/classroom/{classroom.id}/assignments/{assignment.id}/'
        Announcement.objects.create(
            title=f"New Assignment: {assignment.name}",
            content=f"An assignment titled '{assignment.name}' has been added to the classroom.",
            classroom=classroom,
            link=link,
            tutor_link=tutor_link,
        )
    else:
        pass

@receiver(post_save, sender=VideoLecture)
#reciever will get the signal->post_save from sender-> user
#reciever function below will create/update the userProfile accordingly
#immediately after creation/updation of user(sender)
def VideoLecture_post_save(sender, created, instance, **kwargs):
    if created:
        lecture = instance
        playlist = lecture.playlist
        classroom = playlist.classroom
        
        link = f'/classroom/{classroom.id}/LecturePlaylists/{playlist.id}/Lecture/{lecture.id}/'
        Announcement.objects.create(
            title=f"New Lecture: {lecture.name}",
            content=f"An Video Lecture titled '{lecture.name}' has been added to the classroom.",
            classroom=classroom,
            link=link,
        )
    else:
        pass


