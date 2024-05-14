from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify


menu = ["О сайте", "Добавить статью", "Обратная связь", "Войти"]

data_db = [
    {'id':1, 'title': 'Анджелина Джоли', 'content': 'Биография Анджелины Джоли', 'is_published': True},
    {'id':2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id':3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]


# Create your views here.
def index(request):

    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": data_db,
    }
    return render(request, "women/index.html", context=data)


def about(request):
    data = {
        "title": "О нас",
        "menu": menu,
        
    }

    return render(request, "women/about.html", context=data)


def categories(request, cat_id):
    return HttpResponse(f"<h1>Статьи по категориям</h1><p>Категория: {cat_id}</p>")


def categories_by_slug(request, cat_slug):
    print(request.GET)
    return HttpResponse(f"<h1>Статьи по slug</h1><p>Категория: {cat_slug}</p>")


def archive(request, year):
    if year > 2024:
        uri = reverse("cats", args=("music",))
        return redirect(
            uri, permanent=True
        )  # permanent need if code 301 must be else code 302
        # return redirect(index, permanent=True) # permanent need if code 301 must be else code 302
        # return redirect('/', permanent=True) # permanent need if code 301 must be else code 302
    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
