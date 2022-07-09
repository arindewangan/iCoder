from django.contrib import admin
from blog.models import Post
from blog.models import Post, BlogComment

admin.site.register((BlogComment))
@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    class Media:
        js= ('tinyinject.js',)