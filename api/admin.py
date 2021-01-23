from django.contrib import admin

from api.models import Image, Comment, Like


admin.site.register(Image)
admin.site.register(Comment)
admin.site.register(Like)
