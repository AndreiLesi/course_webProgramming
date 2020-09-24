from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post, Comment
from .utils import getPaginator
import json


def index(request):
    # Create new post in database 
    if request.method == "POST":
        newPost = Post(creator=request.user,content=request.POST["content"])
        newPost.save() 

    # Add Pagination
    content = getPaginator(request, Post.objects.order_by("-timestamp"))
    content["currentPage"] = "index"
    return render(request, "network/index.html", content)



def profile(request, username):
    profile = User.objects.get(username=username)

    # Add Pagination
    content = getPaginator(request, profile.posts.order_by("-timestamp"))
    content["profile"] = profile
    return render(request, "network/profile.html", content)



@login_required(login_url="/login")
def following(request):
    # Create empty queryset 
    posts = request.user.posts.none()
    # Merge all querysets (posts form all users) together
    for user in request.user.follows.all():
        posts = posts | user.posts.all() 

    # Add Paginator
    content = getPaginator(request, posts.order_by("-timestamp"))
    content["currentPage"] = "following"
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

def post(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == "POST":
        # Add comment to the database if made
        if "comment" in request.POST.keys():
            comment = Comment(creator=request.user, 
                              content=request.POST["comment"],
                              post=post)
            comment.save()

    # Add Paginator
    content = getPaginator(request, post.comments.order_by("-timestamp"))
    content["comments"] = content.pop("page")
    content["currentPage"] = "comment"
    content["mainPost"] = post
    print(content)

    return render(request, "network/index.html", content)


# API's
@csrf_exempt
@login_required(login_url="/login")
def api_posts(request, post_id):
    # Return post contents
    if request.method == "GET":
        try:
            post = Post.objects.get(creator=request.user, pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        return JsonResponse(post.serialize())

    # Update post content and liked posts
    if request.method == "PUT" and request.user.is_authenticated:
        data = json.loads(request.body)
        # change post content if edited
        if "content" in data:
            # Get post only if creator is the user
            post = Post.objects.get(creator=request.user, pk=post_id)
            post.content = data["content"]
        # or add post to users like list
        elif "like" in data:
            post = Post.objects.get(pk=post_id)
            if request.user in post.likes.all():
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
        post.save()
        return HttpResponse(status=204)

    # post must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)


@csrf_exempt
@login_required(login_url="/login")
def api_follow(request):
    # Update post content and liked posts
    if request.method == "PUT" and request.user.is_authenticated:
        data = json.loads(request.body)
        profile = User.objects.get(id=data["profile_id"])
        if profile in request.user.follows.all():
            request.user.follows.remove(profile)
        else:
            request.user.follows.add(profile)
        request.user.save()
        return HttpResponse(status=204)
    
    # post must be via PUT
    else:
        return JsonResponse({
            "error": "Only PUT request premitted."
        }, status=400)