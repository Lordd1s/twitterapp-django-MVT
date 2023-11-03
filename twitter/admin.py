from django.contrib import admin
from grappelli.forms import GrappelliSortableHiddenMixin

from twitter import models

# Register your models here.


admin.site.register(models.UserProfile)
admin.site.register(models.CommentRatings)
admin.site.register(models.Comment)
admin.site.register(models.Ratings)


class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "title", "date_created", "is_moderate")
    list_filter = ("author", "date_created", "is_moderate")
    list_editable = ("title", "is_moderate")
    search_fields = ("author", "title", "description")


admin.site.register(models.Post, PostAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "recipient",
        "subject",
        "timestamp",
        "answered",
        "replied",
        "is_deleted",
        "is_edited",
        "is_opened",
        "is_viewed",
    )
    list_filter = (
        "sender",
        "recipient",
        "answered",
        "replied",
        "is_deleted",
        "is_edited",
        "is_opened",
        "is_viewed",
    )


admin.site.register(models.Message, MessageAdmin)
