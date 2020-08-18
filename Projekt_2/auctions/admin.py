from django.contrib import admin
from .models import User, Comment, Listing, Bid
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist",)


class ListingAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass


class BidAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Bid)
