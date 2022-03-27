from django.contrib import admin
from .models import blogPost
# Register your models here.
@admin.register(blogPost)

class postModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','description']
