from django.contrib import admin

from media_service.models import Follow, Comment, Like, Post, Profile

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Follow)
