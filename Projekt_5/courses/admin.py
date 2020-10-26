from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Course, Comment, Rating
from django.forms import Textarea, TextInput
from django.db import models
from .models import User

# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    filter_horizontal = ("likes", "enrolled")
    
    # list_display = ('username', 'first_name', 'is_staff',)
    # list_filter = ('username', 'first_name', 'is_staff',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username',  'likes', 'enrolled', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')}),
        # ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = ((None, {'fields': ('first_name', 'last_name', 'username', 'password1', 'password2')}),
    )
    # search_fields = ('email',)
    # ordering = ('email',)


class CommentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }



admin.site.register(User, CustomUserAdmin)
admin.site.register(Course, CommentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Rating, CommentAdmin)
