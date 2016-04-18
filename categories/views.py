from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.core import serializers

from .models import Category

# Create your views here.


def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'Categories/categories_list.html', context)

def category_json(request):
    categories = Category.objects.all()
    return HttpResponse(serializers.serialize('json', categories), content_type="application/json")
