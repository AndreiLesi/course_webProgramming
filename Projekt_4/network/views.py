from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import User, Post, Comment


def index(request):
    # Create new post in database 
    if request.method == "POST":
        newPost = Post(creator=request.user,content=request.POST["content"])
        newPost.save() 

    # Add Pagination
    p = Paginator(Post.objects.order_by("-timestamp"), 5)
    page_number = request.GET.get("page", 1)
    page = p.get_page(page_number)

    # Set previous page URL 
    if page.has_previous():
        previousURL = f"?page={page.previous_page_number()}"
    else:
        previousURL = ''

    # Set next page URL 
    if page.has_next():
        nextURL = f"?page={page.next_page_number()}"
    else:
        nextURL = ''

    content = {"page": page, "previousURL": previousURL, "nextURL": nextURL}
    return render(request, "network/index.html", content)



def profile(request, username):
    user = User.objects.get(username=username)
    print("user:", user)
    print("request:", request.user)
    if request.user == user:
        showFollow = 0
    elif request.user.username in user.followers.all():
        showFollow = 1
    else:
        showFollow = 2

    content = {"profile": user, "showFollow": showFollow}
    return render(request, "network/profile.html", content)



@login_required(login_url="/login")
def following(request):
    # Create empty queryset 
    posts = request.user.posts.none()
    # Merge all querysets (posts form all users) together
    for user in request.user.follows.all():
        posts = posts | user.posts.all() 
    content = {"posts": posts.order_by("-timestamp")}
    return render(request, "network/index.html", content)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
