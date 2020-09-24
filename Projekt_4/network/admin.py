from django.contrib import admin
from .models import User, Post, Comment
from django.forms import Textarea, TextInput
from django.db import models

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("likes", "follows")


class CommentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }



admin.site.register(User, UserAdmin)
admin.site.register(Post, CommentAdmin)
admin.site.register(Comment, CommentAdmin)
