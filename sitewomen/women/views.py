from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Страница приложения women")

def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>Категория: {cat_id}</p>")


def categories_by_slug(request, cat_slug):
    return HttpResponse(f"<h1>Статьи по slug</h1><p>Категория: {cat_slug}</p>")

def archive(request, year):
    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')