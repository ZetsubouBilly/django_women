from typing import Any
from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from .models import Category, Husband



# @deconstructible # только если многократно использовать
# class RussianValidator():
#     ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
#     code = 'russian'

#     def __init__(self, message=None):
#         self.message = message if message else "Должны присутствовать только русские символы, дефис и пробел."

    
#     def __call__(self, value, *args, **kwds):
#         if not(set(value) <= set(self.ALLOWED_CHARS)):
#             raise ValidationError(self.message, code=self.code)

class AddPostForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=5, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}),
                            #  validators=[RussianValidator(),],
                               error_messages={'min_Length': 'Слишком короткий заголовок', 'required': 'Без заголовка никак('})
    slug = forms.SlugField(max_length=255, label="URL", validators=[MinLengthValidator(5, message='Минимум 5 символов'), MaxLengthValidator(100, message='Максимум 100 символов')])
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 5}), label="Содержание")
    is_published = forms.BooleanField(label="Опубликовать", initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Не выбрана", label="Категория")
    husband = forms.ModelChoiceField(queryset=Husband.objects.all(), label="Муж",empty_label="Не замужем", required=False)
    # tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label="Теги", required=False)

    def clean_title(self): # только если нужно проверить конкретное поле
        title = self.cleaned_data['title']
        ALLOWED_CHARS = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "

        if not(set(title) <= set(ALLOWED_CHARS)):
            raise ValidationError("Должны присутствовать только русские символы, дефис и пробел.")

        # return super().clean()