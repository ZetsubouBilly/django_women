import io
from rest_framework import serializers
# from rest_framework.renderers import JSONRenderer, JSONParser
from .models import Women


# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

class WomenSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    slug = serializers.SlugField(max_length=255)
    photo = serializers.ImageField(required=False, allow_null=True, allow_empty_file=True)  # Позволяет `null` и `blank`
    content = serializers.CharField(required=False)  # Позволяем пустой контент
    time_create = serializers.DateTimeField(read_only=True)  # Чтение только
    time_update = serializers.DateTimeField(read_only=True)  # Чтение только
    is_published = serializers.BooleanField(default=False)  # Устанавливаем по умолчанию на DRAFT
    cat_id = serializers.IntegerField()  # Идентификатор категории
    # tags = serializers.ListField(child=serializers.CharField(), required=False)  # Список идентификаторов тегов
    husband_id = serializers.IntegerField(required=False, allow_null=True)  # Идентификатор мужа
    author_id = serializers.IntegerField(required=False, allow_null=True)  # Идентификатор автора


# def encode():
#     model = WomenModel('Andelina', 'Content: Angelina bio')
#     model_sr = WomenSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)


# def decode():
#     stream = io.BytesIO(b'{"title": "Andelina", "content": "Content: Angelina bio"}')
#     data = JSONParser().parse(stream)
#     serializer = WomenSerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)