from django.db import models
from accounts.models import User

class Video(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'mentor'})
    title = models.CharField(max_length=100)
    video_file = models.FileField(upload_to='videos/')
    caption = models.TextField()
    course = models.CharField(max_length=50)

class Note(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'mentor'})
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='notes/')
    course = models.CharField(max_length=50)

class YoutubeLink(models.Model):
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'mentor'})
    title = models.CharField(max_length=100)
    url = models.URLField()
    course = models.CharField(max_length=50)

class Message(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_msg', limit_choices_to={'role': 'student'})
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_msg', limit_choices_to={'role': 'mentor'})
    question = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class VideoWatch(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_on = models.DateTimeField(auto_now_add=True)
