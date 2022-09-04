from django.contrib import admin
from base.models import Category, Article, Comments


# class TagAdmin(admin.ModelAdmin):
# 	prepopulated_fields = {"slug":("title",)}

class ArticleAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":("title",)}

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug":("title",)}

class CommentAdmin(admin.ModelAdmin):
	list_display = ['article','full_name'] 
	list_filter = ['article']
	

admin.site.register(Category, CategoryAdmin)
# admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comments, CommentAdmin)