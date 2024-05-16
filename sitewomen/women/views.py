from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .models import Women


menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add_page'},
    {'title': 'Обратная связь', 'url_name': 'contact'},
    {'title': 'Войти', 'url_name': 'login'},
]

data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<h1>Анджелина Джоли</h1> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.
    Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id':2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id':3, 'title': 'Джулия Робертс', 'content': 'Биография Джулии Робертс', 'is_published': True},
]

cats_db = [
      {'id': 1, 'name': 'Актрисы',},
      {'id': 2, 'name': 'Певицы',},
      {'id': 3, 'name': 'Спортсменки',},
]


# Create your views here.
def index(request):
    posts = Women.objects.filter(is_published=1)
    data = {
        "title": "Главная страница",
        "menu": menu,
        "posts": posts,
        'cat_selected': 0,
    }
    return render(request, "women/index.html", context=data)


def about(request):
    data = {
        "title": "О нас",
        "menu": menu,
        
    }

    return render(request, "women/about.html", context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
          'title': post.title,
          'menu': menu,
          'post': post,
          'cat_selected': 1,
    }
    return render(request, "women/post.html", context=data)


def addpage(request):
        return HttpResponse(f'Добавление статьи')

def contact(request):
        return HttpResponse(f'Обратная связь')

def login(request):
        return HttpResponse(f'Авторизация')

def show_category(request, cat_id):
    data = {
        "title": "Отображение по рубрикам",
        "menu": menu,
        "posts": data_db,
        'cat_selected': cat_id,
    }
    return render(request, "women/index.html", context=data)

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
