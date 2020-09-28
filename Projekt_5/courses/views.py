from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import UserForm, CourseForm
from .models import User, Course, Comment

# Create your views here.
def index(request):
    content = {"page": 1}
    return render(request, "courses/index.html", content)


def courses(request, coursesCategory):
    print("in courses")
    # Display all available courses
    if coursesCategory == "All":
        courses = Course.objects.all()
        htmlHeading = "Our Courses"
    # Display only the enrolles courses 
    elif coursesCategory == "Enrolled" and request.user.is_authenticated:
        courses = request.user.enrolled.all()
        htmlHeading = "Enrolled Courses"
    # Redirect to categories page
    elif coursesCategory == "Categories":
        htmlHeading = "Course Topics"
        topics = [course[0] for course in Course.topics]
        content = {"topics":topics, "htmlHeading":htmlHeading}
        return render(request, "courses/courses_categories.html", content)
    # If topic exists filter only those courses, else 
    else:
        choices = [course[0] for course in Course.topics]
        courses = Course.objects.filter(topic=coursesCategory)
        if coursesCategory in choices:
            htmlHeading = f"{coursesCategory} Courses"
        else:
            htmlHeading = "Undefined Course Topic"
    content = {"courses": courses, "htmlHeading":htmlHeading}
    return render(request, "courses/courses.html", content)


def course_details(request, course_id):
    course = Course.objects.get(id=course_id)
    content = {"course": course}
    return render(request, "courses/course_details.html", content)
    

def course_create(request):
    form = CourseForm(request.POST or None)

    if request.method == "POST":
        # create a new Listing if all the inputs are valid and display it
        if form.is_valid():
            courseModel = form.save(commit=False)
            courseModel.creator = request.user
            print("Form cleaned:", form.cleaned_data)
            if form.cleaned_data["imageLink"]:
                print("NewImageLink")
                courseModel.image = form.cleaned_data["imageLink"]
            courseModel.save()
            return redirect("course_details", course_id = courseModel.id)

    return render(request, "courses/course_create.html", {
        'form': form
    })


def about(request):
    content = {"page": 1}
    return render(request, "courses/about.html", content)


def contact(request):
    content = {"page": 1}
    return render(request, "courses/contact.html", content)


def blog(request):
    content = {"page": 1}
    return render(request, "courses/blog.html", content)


def blog_details(request):
    content = {"page": 1}
    return render(request, "courses/blog_details.html", content)


def elements(request):
    content = {"page": 1}
    return render(request, "courses/elements.html", content)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "courses/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "courses/login.html")

def register(request):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()

    content = {"form": form}
    return render(request, "courses/register.html", content)