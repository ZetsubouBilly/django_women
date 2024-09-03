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

    def create(self, validated_data):
        return Women.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.slug = validated_data.get('slug', instance.slug)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.content = validated_data.get('content', instance.content)
        instance.time_update = validated_data.get('time_update', instance.time_update)
        instance.is_published = validated_data.get('is_published', instance.is_published)
        instance.cat_id = validated_data.get('cat_id', instance.cat_id)
        instance.husband_id = validated_data.get('husband_id', instance.husband_id)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.save()
        return instance

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