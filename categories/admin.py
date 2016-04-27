from django.contrib import admin
from django_mptt_admin.admin import DjangoMpttAdmin


from .models import Category


# Register your models here.

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
