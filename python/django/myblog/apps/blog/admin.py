from models import Post,Category
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'description')

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'date', 'author', 'status')
    list_filter = ('date', 'author', 'category', 'type', 'status')
    radio_fields = { 
        'status': admin.VERTICAL,
        'type': admin.VERTICAL
    }   
    search_fields = ('title', 'author', 'content')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
