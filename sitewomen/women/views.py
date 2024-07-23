
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .utils import DataMixin

from django.core.paginator import Paginator

# from django.template.loader import render_to_string
# from django.template.defaultfilters import slugify


from .forms import AddPostForm, UploadFileForm

from .models import TagPost, UploadFiles, Women, Category





class WomenHome(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    title_page = "Главная страница"
    cat_selected = 0
    

    def get_queryset(self):
        return Women.published.all().select_related("cat")




def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list,3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
            
    #         fp = UploadFiles(file=form.cleaned_data["file"])
    #         fp.save()
    # else:
    #     form = UploadFileForm()
    # data = {"title": "О нас",  "form": form}
    data = {"title": "О нас",  "page_obj": page_obj}

    return render(request, "women/about.html", context=data)



class ShowPost(DataMixin, DetailView):
    template_name = "women/post.html"
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)
        
    
    def get_object(self, queryset=None):

        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])






class AddPage(DataMixin, CreateView):
    form_class = AddPostForm  
    template_name = "women/addpage.html"
    title_page = "Добавление статьи"
    success_url = reverse_lazy("home")
    


class UpdatePage(DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    title_page = "Редактирование статьи"
    success_url = reverse_lazy("home")
   

class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Удаление статьи"
    


def contact(request):
    return HttpResponse(f"Обратная связь")


def login(request):
    return HttpResponse(f"Авторизация")




class WomenCategory(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    allow_empty = False
    

    def get_queryset(self):
        
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - '+ cat.name, cat_selected=cat.pk)
        




class WomenTag(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    allow_empty = False


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег - '+ tag.tag)
        

    def get_queryset(self):       
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related("cat")

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
