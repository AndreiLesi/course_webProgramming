from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("index", views.index, name='index'),
    path("courses/upload", views.course_create, name='course_create'),
    path("courses/<str:coursesCategory>", views.courses, name='courses'),
    path("course_details/<int:course_id>", views.course_details, name='course_details'),
    path("profile/<str:username>", views.profile, name='profile'), 
    path("about", views.about, name='about'), 
    path("blog", views.blog, name='blog'), 
    path("blog_details", views.blog_details, name='blog_details'), 
    path("elements", views.elements, name='elements'), 
    path("contact", views.contact, name='contact'), 
    path("login", views.login_view, name='login'), 
    path("register", views.register, name='register'), 
]
