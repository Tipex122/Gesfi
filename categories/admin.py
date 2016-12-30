from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin
from .models import Category, Tag


# Register your models here.

class TagAdmin(admin.ModelAdmin):
    fieldsets  = [
        (None, {'fields': ['tag',]}),
        ('Info Genre',
         {'fields': ['category','will_be_used_as_tag', 'is_new_tag',]}),
    ]
    list_display = ('tag', 'is_new_tag', 'will_be_used_as_tag', 'category')
    search_fields = ['tag', 'category']
    list_filter = ('category', 'will_be_used_as_tag', 'is_new_tag',)

admin.site.register(Tag, TagAdmin)
#admin.site.register(Tag)


class CategoryAdmin(DjangoMpttAdmin ):
    #    fields = ['name', 'description', 'amount', 'parent']
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Info Catégorie', {'fields': ['parent', 'description', 'amount']}),
#        ('Tags associés', {'fields': ['tag',]})
    ]
    list_display = ('name', 'amount', 'parent',)
    search_fields = ['name', 'amount', ]
    list_filter = ('parent',)


# mptt_level_indent = 20

admin.site.register(Category, CategoryAdmin)
