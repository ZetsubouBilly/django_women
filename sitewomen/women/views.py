from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Страница приложения women")

def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>Категория: {cat_id}</p>")


def categories_by_slug(request, cat_slug):
    print(request.GET)
    return HttpResponse(f"<h1>Статьи по slug</h1><p>Категория: {cat_slug}</p>")

def archive(request, year):
    if year > 2024:
        raise Http404()
    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")