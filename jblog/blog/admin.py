from django.contrib import admin
from blog.models import Post, Comment, Tag, Category

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

