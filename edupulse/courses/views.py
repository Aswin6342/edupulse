from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Video, Note, YoutubeLink, VideoWatch, Message
from accounts.models import User

@login_required
def mentor_uploads(request):
    if request.user.role != "mentor":
        return redirect("dashboard")
    
    if request.method == "POST":
        if 'video' in request.POST:
            try:
                Video.objects.create(
                    mentor=request.user,
                    title=request.POST['title'],
                    video_file=request.FILES['video_file'],
                    caption=request.POST['caption'],
                    course=request.user.course
                )
                messages.success(request, 'Video uploaded successfully!')
            except Exception as e:
                messages.error(request, f'Error uploading video: {str(e)}')
        elif 'note' in request.POST:
            try:
                Note.objects.create(
                    mentor=request.user,
                    title=request.POST['title'],
                    file=request.FILES['file'],
                    course=request.user.course
                )
                messages.success(request, 'Note uploaded successfully!')
            except Exception as e:
                messages.error(request, f'Error uploading note: {str(e)}')
        elif 'youtube' in request.POST:
            try:
                YoutubeLink.objects.create(
                    mentor=request.user,
                    title=request.POST['title'],
                    url=request.POST['url'],
                    course=request.user.course
                )
                messages.success(request, 'YouTube link added successfully!')
            except Exception as e:
                messages.error(request, f'Error adding YouTube link: {str(e)}')
    
    return render(request, "courses/mentor_uploads.html")

@login_required
def student_videos(request):
    if request.user.role != "student":
        return redirect("dashboard")
    videos = Video.objects.filter(course=request.user.course)

    # Mark video as watched
    if request.method == "POST":
        video_id = request.POST.get("video_id")
        video = get_object_or_404(Video, id=video_id)
        VideoWatch.objects.get_or_create(student=request.user, video=video)
        messages.success(request, 'Video marked as watched!')
    
    watched_videos = VideoWatch.objects.filter(student=request.user).values_list('video_id', flat=True)
    return render(request, "courses/student_videos.html", {
        "videos": videos,
        "watched_videos": watched_videos
    })

@login_required
def student_notes(request):
    if request.user.role != "student":
        return redirect("dashboard")
    notes = Note.objects.filter(course=request.user.course)
    return render(request, "courses/student_notes.html", {"notes": notes})

@login_required
def student_youtube(request):
    if request.user.role != "student":
        return redirect("dashboard")
    links = YoutubeLink.objects.filter(course=request.user.course)
    return render(request, "courses/student_youtube.html", {"links": links})

@login_required
def student_performance(request):
    if request.user.role != "student":
        return redirect("dashboard")
    total_videos = Video.objects.filter(course=request.user.course).count()
    watched = VideoWatch.objects.filter(student=request.user).count()
    return render(request, "courses/student_performance.html", {
        "total": total_videos,
        "watched": watched
    })

# Student → send doubts to mentor
@login_required
def student_messages(request):
    if request.user.role != "student":
        return redirect("dashboard")
    
    mentor = User.objects.filter(role="mentor", course=request.user.course).first()  # student's mentor
    
    if request.method == "POST":
        question = request.POST.get("question")
        if mentor and question.strip():
            Message.objects.create(student=request.user, mentor=mentor, question=question)
            messages.success(request, 'Message sent successfully!')
    
    messages_list = Message.objects.filter(student=request.user).order_by('-created_at')
    return render(request, "courses/student_messages.html", {"messages": messages_list})

# Mentor → view & reply to student doubts
@login_required
def mentor_messages(request):
    if request.user.role != "mentor":
        return redirect("dashboard")

    messages_list = Message.objects.filter(mentor=request.user).order_by('-created_at')

    if request.method == "POST":
        msg_id = request.POST.get("msg_id")
        reply_text = request.POST.get("reply")
        try:
            msg = Message.objects.get(id=msg_id, mentor=request.user)
            msg.reply = reply_text
            msg.save()
            messages.success(request, 'Reply sent successfully!')
        except Message.DoesNotExist:
            messages.error(request, 'Message not found!')

    return render(request, "courses/mentor_messages.html", {"messages": messages_list})
