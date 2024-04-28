from django.dispatch import receiver
from django.db.models.signals import pre_delete
from classroom.models import VideoLecture, Playlist, Announcement, LectureNote


@receiver(pre_delete, sender=VideoLecture)
def lecture_pre_delete(sender, instance, **kwargs):    
    lecture = instance
    classroom = lecture.playlist.classroom
    #deleting all notes of the lecture
    notes = LectureNote.objects.filter(video_lecture=lecture)
    if notes:
        for note in notes:
            note.note_file.delete() 
            note.delete()
        else:
            pass

    #deleting announcement of that lecture if exist
    try:
        link = f'/classroom/{classroom.id}/LecturePlaylists/{lecture.playlist.id}/'
        announcement = Announcement.objects.get(link=link)
        announcement.delete()
    except:
        pass

@receiver(pre_delete, sender=Playlist)
def playlist_pre_delete(sender, instance, **kwargs):    
    playlist = instance
    #deleting all lectures of the playlist
    lectures = VideoLecture.objects.filter(playlist=playlist)
    for lecture in lectures:
        lecture.delete() 
        #this lecture delete will trigger the lecture pre delete
        #so lecture delete will taken care by that 
