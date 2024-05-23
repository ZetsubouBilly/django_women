from django import forms
from .models import Category, Husband


class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length=255, label="URL")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), label="Содержание")
    is_published = forms.BooleanField(label="Опубликовать", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрана", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label="Муж",empty_label="Не замужем", required=False)
    # tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label="Теги", required=False)