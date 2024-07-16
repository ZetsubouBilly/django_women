import os
import uuid
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, ListView

# from django.template.loader import render_to_string
# from django.template.defaultfilters import slugify


from .forms import AddPostForm, UploadFileForm

from .models import TagPost, UploadFiles, Women, Category


menu = [
    {"title": "О сайте", "url_name": "about"},
    {"title": "Добавить статью", "url_name": "add_page"},
    {"title": "Обратная связь", "url_name": "contact"},
    {"title": "Войти", "url_name": "login"},
]


# Create your views here.
# def index(request):
#     posts = Women.published.all().select_related("cat")
#     data = {
#         "title": "Главная страница",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": 0,
#     }
#     return render(request, "women/index.html", context=data)


class WomenHome(ListView):
    # model = Women
    template_name = "women/index.html"
    context_object_name = 'posts'
    extra_context = {
        "title": "Главная страница",
        "menu": menu,
        "cat_selected": 0,
    }

    def get_queryset(self):
        return Women.published.all().select_related("cat")

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['posts'] = Women.published.all().select_related("cat")
    #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0))
    #     return context

# def handle_uploaded_file(f):
#     directory = 'uploads'
#     unique_filename = str(uuid.uuid1())
#     if not os.path.exists(directory):
#         os.makedirs(directory)

#     with open(f'uploads/{unique_filename}', 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(form.cleaned_data['file'])
            fp = UploadFiles(file=form.cleaned_data["file"])
            fp.save()
    else:
        form = UploadFileForm()
    data = {"title": "О нас", "menu": menu, "form": form}

    return render(request, "women/about.html", context=data)


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)

    data = {
        "title": post.title,
        "menu": menu,
        "post": post,
        "cat_selected": 1,
    }
    return render(request, "women/post.html", context=data)


# def addpage(request):
#     if request.method == "POST":
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # try:
#             #     Women.objects.create(**form.cleaned_data)
#             #     return redirect("home")
#             # except:
#             #     form.add_error(None, "Ошибка добавления поста")
#             #     return HttpResponse(f"Не удалось добавить запись в базу данных")
#             form.save()
#             return redirect("home")
#     else:
#         form = AddPostForm()

#     data = {"menu": menu, "title": "Добавление статьи", "form": form}
#     return render(request, "women/addpage.html", data)


class AddPage(View):
    def get(self, request):
        form = AddPostForm()
        data = {"menu": menu, "title": "Добавление статьи", "form": form}
        return render(request, "women/addpage.html", data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

        data = {"menu": menu, "title": "Добавление статьи", "form": form}
        return render(request, "women/addpage.html", data)


def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug)
#     posts = Women.published.filter(cat_id=category.pk).select_related("cat")
#     data = {
#         "title": f"Рубрика: {category.name}",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": category.pk,
#     }
#     return render(request, "women/index.html", context=data)


class WomenCategory(ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - '+ cat.name
        context['menu'] = menu        
        context['cat_selected'] = cat.pk
        return context


# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related("cat")

#     data = {
#         "title": f"Тег: {tag.tag}",
#         "menu": menu,
#         "posts": posts,
#         "cat_selected": None,
#     }

#     return render(request, "women/index.html", context=data)


class WomenTag(ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):       
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег - '+ tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    # def get_queryset(self):       
    #     self.tag = get_object_or_404(TagPost, slug=self.kwargs['tag_slug'])
    #     return self.tag.tags.filter(is_published=1).select_related('cat')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = f'Посты с тегом - {self.tag.tag}'
    #     context['menu'] = menu
    #     context['cat_selected'] = 0
    #     return context

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
