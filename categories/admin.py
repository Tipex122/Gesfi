from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Tag


# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fieldsets  = [
        (None, {'fields': ['tag',]}),
        ('Info Genre',
         {'fields': ['category',]}),
    ]
    list_display = ('tag', 'category')
    search_fields = ['tag', 'category']
    list_filter = ('tag', 'category',)

admin.site.register(Tag, TagAdmin)
#admin.site.register(Tag)


class CategoryAdmin(DjangoMpttAdmin ):
    #    fields = ['name', 'description', 'amount', 'parent']
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Info Catégorie', {'fields': ['parent', 'description', 'amount']}),
    ]
    list_display = ('name', 'amount', 'parent',)
    search_fields = ['name', 'amount', ]
    list_filter = ('parent',)


# mptt_level_indent = 20

admin.site.register(Category, CategoryAdmin)
