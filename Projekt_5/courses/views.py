from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import UserForm, CourseForm
from .models import User, Course, Comment, Rating
from .utils import getPaginator
from django.db.models import Avg, Count


# Create your views here.
def index(request):
    topCourses = Course.objects.order_by('-timestamp').annotate(
                    avg_rating=Avg('ratings__rating'),  
                    num_ratings=Count('ratings__rating'),)
    topCourses = topCourses.order_by("-avg_rating")[0:10]

    topics = [course[0] for course in Course.topics]
    content = {"topics": topics, "topCourses":topCourses}
    return render(request, "courses/index.html", content)


def courses(request, coursesCategory):
    # Display all available courses
    if coursesCategory == "All":
        courses = Course.objects.order_by('-timestamp').annotate(
                  avg_rating=Avg('ratings__rating'),  
                  num_ratings=Count('ratings__rating'),)
        content = getPaginator(request, courses, 9)
        htmlHeading = "All our Courses"
    # Display only the enrolles courses 
    elif coursesCategory == "Enrolled" and request.user.is_authenticated:
        courses = request.user.enrolled.order_by("-timestamp").annotate(
                  avg_rating=Avg('ratings__rating'),
                  num_ratings=Count('ratings__rating'),)
        content = getPaginator(request, courses, 9)
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
        courses = Course.objects.filter(topic=coursesCategory)\
                  .order_by("-timestamp").annotate(
                   avg_rating = Avg('ratings__rating'),
                   num_ratings=Count('ratings__rating'),)
        content = getPaginator(request, courses, 9)
        if coursesCategory in choices:
            htmlHeading = f"{coursesCategory} Courses"
        else:
            htmlHeading = "Undefined Course Topic"
    content["htmlHeading"] = htmlHeading
    return render(request, "courses/courses.html", content)


def course_details(request, course_id):
    course = Course.objects.get(id=course_id)
    content = {"course": course}

    if request.method == "POST":
        # Add Comment to database if present
        if "content" in request.POST.keys():
            comment = Comment()
            comment.content = request.POST["content"]
            comment.creator = request.user
            comment.course = course
            comment.save()

            # Add Rating to database if present
            if "rating" in request.POST.keys():
                rating = Rating()
                rating.creator = request.user
                rating.course = course
                rating.rating = int(request.POST["rating"])
                rating.save()

        # Enroll/De-enroll user from course
        elif "buyCourse" in request.POST.keys():
            print(f"buyCourse: {request.POST}")
            if course in request.user.enrolled.all():
                request.user.enrolled.remove(course)
            else:
                request.user.enrolled.add(course)
            request.user.save()

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


def profile(request, profile_id):
    profile = User.objects.get(id=profile_id)

    # Add Pagination
    content = getPaginator(request, profile.uploadedCourses\
                .order_by("-timestamp").annotate(
                avg_rating=Avg('ratings__rating'),  
                num_ratings=Count('ratings__rating'),), 10)
    content["profile"] = profile
    return render(request, "courses/profile.html", content)


def contact(request):
    content = {"page": 1}
    return render(request, "courses/contact.html", content)


def elements(request):
    content = {"page": 1}
    return render(request, "courses/elements.html", content)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    form = UserForm()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            user = User.objects.get(username=form.cleaned_data["username"]) 
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    content = {"form": form}
    return render(request, "courses/register.html", content)