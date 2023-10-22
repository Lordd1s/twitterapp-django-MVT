from django.contrib import admin

from twitter import models

# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.Message)
admin.site.register(models.UserProfile)
admin.site.register(models.CommentRatings)
admin.site.register(models.Comment)
admin.site.register(models.Ratings)
