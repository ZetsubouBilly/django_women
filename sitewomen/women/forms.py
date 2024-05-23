from django import forms
from .models import Category, Husband


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок")
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea, label="Содержание")
    is_published = forms.BooleanField(label="Опубликовать")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label="Муж", required=False)
    # tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label="Теги", required=False)