from django.contrib import admin

from .models import Recipe, Comment, TipTrick, Photo

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Comment)
admin.site.register(TipTrick)
admin.site.register(Photo)