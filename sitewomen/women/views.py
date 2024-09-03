
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet

from django.forms import model_to_dict
from django.http import  HttpResponse, HttpResponseNotFound

from django.shortcuts import get_object_or_404, render

from django.urls import  reverse_lazy

from django.views import View
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView, DeleteView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.core.cache import cache
from django.core.paginator import Paginator

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import TagPost, UploadFiles, Women, Category
from .serializers import WomenSerializer
from .utils import DataMixin
from .forms import AddPostForm, UploadFileForm, ContactForm

from http import HTTPStatus




class WomenHome(DataMixin, ListView):
    template_name = "women/index.html"
    context_object_name = 'posts'
    title_page = "Главная страница"
    cat_selected = 0
    

    def get_queryset(self):
        w_lst = cache.get('women_posts')
        if not w_lst:
            w_lst = Women.published.all().select_related("cat")
            cache.set('women_posts', w_lst, 60)
        return Women.published.all().select_related("cat")



@login_required
def about(request):
    contact_list = Women.published.all()
    paginator = Paginator(contact_list,3)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

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


class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm  
    template_name = "women/addpage.html"
    title_page = "Добавление статьи"
    permission_required = 'women.add_women'
    success_url = reverse_lazy("home")
    # login_url = '/admin/'
    
    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):
    model = Women
    fields = ["title", "content", "photo", "is_published", "cat"]
    template_name = "women/addpage.html"
    title_page = "Редактирование статьи"
    permission_required = 'women.change_women'

    success_url = reverse_lazy("home")
   

class DeletePage(DataMixin, DeleteView):
    model = Women
    template_name = "women/addpage.html"
    success_url = reverse_lazy("home")
    title_page = "Удаление статьи"
    

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = "women/contact.html"
    success_url = reverse_lazy('home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

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


# class WomenApiView(generics.ListAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer


class WomenApiView(APIView):
    def get(self, request):
        w = Women.objects.all()
        return Response({'posts': WomenSerializer(w, many=True).data})
    
    def post(self, request):
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        try:
            
            return Response({'post': serializer.data}, status=HTTPStatus.CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=HTTPStatus.BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method PUT not allowed'})
        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({'error': 'Object does not exist'})
        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'error': 'Method DELETE not allowed'})
        try:
            instance = Women.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({'error': 'Object does not exist'})
        return Response({'post': 'delete post ' + str(pk)})
