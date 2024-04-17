from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from classroom.models import Announcement, Assignment, AssignmentSubmission
  
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

@receiver(pre_delete, sender=Assignment)
def assignment_pre_delete(sender, instance, **kwargs):    
    assignment = instance
    classroom = assignment.classroom
    #deleting assignment file and all submission files of that assignment
    assignment.assignment.delete()
    submitted_assignments=AssignmentSubmission.objects.filter(assignment=assignment)
    for file in submitted_assignments:
        file.submitted_file.delete()
    #deleting announcement of that assignment if exist
    try:
        link = f'/classroom/{classroom.id}/assignments/{assignment.id}/'
        announcement = Announcement.objects.get(link=link)
        announcement.delete()
    except:
        pass
