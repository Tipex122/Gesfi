from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category

# Create your views here.


def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'Categories/categories_list.html', context)
