from django.urls import path
from . import views

urlpatterns = [
    path('mentor/uploads/', views.mentor_uploads, name='mentor_uploads'),
    path('mentor/messages/', views.mentor_messages, name='mentor_messages'),
    path('student/videos/', views.student_videos, name='student_videos'),
    path('student/notes/', views.student_notes, name='student_notes'),
    path('student/youtube/', views.student_youtube, name='student_youtube'),
    path('student/performance/', views.student_performance, name='student_performance'),
    path('student/messages/', views.student_messages, name='student_messages'),
]
