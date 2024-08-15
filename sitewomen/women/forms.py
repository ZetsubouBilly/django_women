from typing import Any
from django import forms
from captcha.fields import CaptchaField
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from .models import Category, Husband, Women



# @deconstructible # только если многократно использовать
# class RussianValidator():
#     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#     code = 'russian'

#     def __init__(self, message=None):
#         self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    
#     def __call__(self, value, *args, **kwds):
#         if not(set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.ModelForm):
   
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрана", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label="Муж",empty_label="Не замужем", required=False)
    # tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label="Теги", required=False)

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content','photo','is_published', 'cat', 'husband', 'tags']
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }
        labels = {'slug': 'URL'}


    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 100:
            raise ValidationError('Длина превышает 100 символов')
        return title
    

class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Сообщение")
    captcha = CaptchaField()