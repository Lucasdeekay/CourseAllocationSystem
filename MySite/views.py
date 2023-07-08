from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from MySite.models import Lecturer, CourseAllocation, Department, Course


# Create your views here.
class LoginView(View):
    template_name = "mysite/login.html"

    def get(self, request):
        # Go to the login page
        return render(request, self.template_name)

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Collect inputs
            username = request.POST.get("staff_id").strip()
            password = request.POST.get("password")

            # Authenticate user
            user = authenticate(username=username, password=password)

            # Check if user exist
            if user is not None:
                # Login user
                login(request, user)
                # Redirect to learning page
                return HttpResponseRedirect(reverse("MySite:home"))
            else:
                # Send error message
                messages.error(request, "Invalid credentials")
                # Redirect to login page
                return HttpResponseRedirect(reverse("MySite:login"))


class RegisterView(View):
    template_name = "mysite/register.html"

    def get(self, request):
        departments = Department.objects.all()
        # Go to the register page
        return render(request, self.template_name, {"departments": departments})

    def post(self, request):
        # Check if form is submitting
        if request.method == "POST":
            # Get user input
            staff_id = request.POST.get('staff_id').strip().upper()
            last_name = request.POST.get('last_name').strip().upper()
            first_name = request.POST.get('first_name').strip().upper()
            email = request.POST.get('email').strip()
            department = request.POST.get('department').strip().upper()
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if not User.objects.filter(username=staff_id).exists() and Department.objects.filter(name__icontains=department).exists():
                if password == confirm_password:
                    user = User.objects.create_user(username=staff_id, password=password)
                    department = Department.objects.get(name__icontains=department)
                    Lecturer.objects.create(user=user, last_name=last_name, first_name=first_name, email=email,
                                            staff_id=staff_id, department=department)

                    messages.success(request, "Registration successful")
                    return HttpResponseRedirect(reverse("MySite:login"))
                else:
                    messages.success(request, "Password dos not match")
                    return HttpResponseRedirect(reverse("MySite:register"))
            else:
                messages.success(request, "User already exists")
                return HttpResponseRedirect(reverse("MySite:register"))


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse("MySite:login"))


class HomeView(View):
    template_name = "mysite/home.html"

    def get(self, request):
        if Lecturer.objects.filter(user=request.user).exists():
            lecturer = Lecturer.objects.get(user=request.user)
            return render(request, self.template_name, {"lecturer": lecturer})
        elif request.user.is_superuser:
            return render(request, self.template_name, {"admin": True})
        else:
            return render(request, self.template_name)


class DashboardView(View):
    template_name = "mysite/dashboard.html"

    @method_decorator(login_required)
    def get(self, request):
        if Lecturer.objects.filter(user=request.user).exists():
            lecturer = Lecturer.objects.get(user=request.user)
            alloc_courses = CourseAllocation.objects.filter(lecturer=lecturer)
            return render(request, self.template_name, {"lecturer": lecturer, "courses": alloc_courses})
        elif request.user.is_superuser:
            return HttpResponseRedirect('MySite:dash_admin')


class DashboardAdminView(View):
    template_name = "mysite/dash_admin.html"

    @method_decorator(login_required)
    def get(self, request):
        if not Lecturer.objects.filter(user=request.user).exists():
            departments = Department.objects.all()
            return render(request, self.template_name, {"departments": departments, "admin": True})
        else:
            return HttpResponseRedirect(reverse("MySite:dashboard"))

    def post(self, request):
        department = request.POST.get("department")
        all_lecturers = Lecturer.objects.filter(department=Department.objects.get(name=department))
        return render(request, self.template_name, {
            "current_dep": department,
            "lecturers": all_lecturers,
            "admin": True
        })


def choose_lecturer(request):
    template_name = "mysite/dash_admin.html"

    if request.method == "POST":
        staff_id = request.POST.get("lecturer")
        staff = Lecturer.objects.get(staff_id=staff_id)
        courses = Course.objects.filter(department=staff.department)
        unalloc_courses = []
        alloc_courses = []
        for course in courses:
            if CourseAllocation.objects.filter(**{"course": course, "lecturer": staff}).exists():
                course = CourseAllocation.objects.get(**{"course": course, "lecturer": staff})
                alloc_courses.append(course)
            if not CourseAllocation.objects.filter(course=course).exists():
                unalloc_courses.append(course)
        return render(request, template_name, {
            "staff": staff,
            "alloc_courses": alloc_courses,
            "unalloc_courses": unalloc_courses,
            "admin": True
        })


def allocate(request, course_id, staff_id):
    template_name = "mysite/dash_admin.html"
    staff = Lecturer.objects.get(staff_id=staff_id)
    course = Course.objects.get(id=course_id)
    if not CourseAllocation.objects.filter(**{"course": course, "lecturer": staff}).exists():
        CourseAllocation.objects.create(course=course, lecturer=staff)
    courses = Course.objects.filter(department=staff.department)
    unalloc_courses = []
    alloc_courses = []
    for c in courses:
        if CourseAllocation.objects.filter(**{"course": c, "lecturer": staff}).exists():
            cor = CourseAllocation.objects.get(**{"course": c, "lecturer": staff})
            alloc_courses.append(cor)
        if not CourseAllocation.objects.filter(course=c).exists():
            unalloc_courses.append(c)
    return render(request, template_name, {
        "staff": staff,
        "alloc_courses": alloc_courses,
        "unalloc_courses": unalloc_courses,
        "admin": True
    })


def deallocate(request, course_id, staff_id):
    template_name = "mysite/dash_admin.html"
    staff = Lecturer.objects.get(staff_id=staff_id)
    course = CourseAllocation.objects.get(id=course_id)
    course.delete()
    courses = Course.objects.filter(department=staff.department)
    unalloc_courses = []
    alloc_courses = []
    for course in courses:
        if CourseAllocation.objects.filter(**{"course": course, "lecturer": staff}).exists():
            course = CourseAllocation.objects.get(**{"course": course, "lecturer": staff})
            alloc_courses.append(course)
        if not CourseAllocation.objects.filter(course=course).exists():
            unalloc_courses.append(course)
    return render(request, template_name, {
        "staff": staff,
        "alloc_courses": alloc_courses,
        "unalloc_courses": unalloc_courses,
        "admin": True
    })
