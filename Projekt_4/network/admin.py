from django.contrib import admin
from .models import User, Post, Comment

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes", "follows")


class PostAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Post)
admin.site.register(Comment)
