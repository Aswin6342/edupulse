from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignupForm

User = get_user_model()

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def create_demo_users(request):
    """Temporary view to create demo users - remove in production"""
    if User.objects.count() == 0:
        # Create superadmin
        superadmin = User.objects.create_user(
            username='superadmin',
            email='superadmin@edupulse.com',
            password='password123',
            role='superadmin'
        )
        superadmin.is_staff = True
        superadmin.is_superuser = True
        superadmin.save()
        
        # Create admin
        admin = User.objects.create_user(
            username='admin1',
            email='admin1@edupulse.com',
            password='password123',
            role='admin'
        )
        admin.is_staff = True
        admin.save()
        
        # Create mentor
        mentor = User.objects.create_user(
            username='mentor1',
            email='mentor1@edupulse.com',
            password='password123',
            role='mentor',
            course='Django'
        )
        
        # Create student
        student = User.objects.create_user(
            username='student1',
            email='student1@edupulse.com',
            password='password123',
            role='student',
            course='Django'
        )
        
        messages.success(request, 'Demo users created successfully!')
    else:
        messages.info(request, 'Demo users already exist!')
    
    return redirect('/')

@login_required
def dashboard(request):
    if request.user.role == 'superadmin':
        return render(request, 'accounts/superadmin_dashboard.html')
    elif request.user.role == 'admin':
        return render(request, 'accounts/admin_dashboard.html')
    elif request.user.role == 'mentor':
        return render(request, 'accounts/mentor_dashboard.html')
    elif request.user.role == 'student':
        return render(request, 'accounts/student_dashboard.html')

@login_required
def add_admin(request):
    if request.user.role != "superadmin":
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username and password:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role="admin"
            )
            return redirect("view_admins")
    return render(request, "accounts/add_admin.html")

@login_required
def view_admins(request):
    if request.user.role != "superadmin":
        return redirect("dashboard")
    admins = User.objects.filter(role="admin")
    return render(request, "accounts/view_admins.html", {"admins": admins})

@login_required
def add_mentor(request):
    if request.user.role != "admin":
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        course = request.POST.get("course")
        if username and password:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role="mentor",
                course=course
            )
            return redirect("view_mentors")
    return render(request, "accounts/add_mentor.html")

@login_required
def view_mentors(request):
    if request.user.role != "admin":
        return redirect("dashboard")
    mentors = User.objects.filter(role="mentor")
    return render(request, "accounts/view_mentors.html", {"mentors": mentors})
