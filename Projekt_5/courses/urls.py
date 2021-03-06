from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("index", views.index, name='index'),
    path("courses/upload", views.course_create, name='course_create'),
    path("courses/<str:coursesCategory>", views.courses, name='courses'),
    path("course_details/<int:course_id>", views.course_details, name='course_details'),
    path("profile/<int:profile_id>", views.profile, name='profile'), 
    path("elements", views.elements, name='elements'), 
    path("contact", views.contact, name='contact'), 
    path("login", views.login_view, name='login'), 
    path("logout", views.logout_view, name='logout'), 
    path("register", views.register, name='register'), 
]
