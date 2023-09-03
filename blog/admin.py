from django.contrib import admin

# Register your models here.
from .models import Post
@admin.register(Post)
class PostmodelAdmin(admin.ModelAdmin):
    list_display=['id','title','desc']