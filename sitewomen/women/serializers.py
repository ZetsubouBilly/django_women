import io
from rest_framework import serializers
# from rest_framework.renderers import JSONRenderer, JSONParser
from .models import Women


# class WomenModel:
#     def __init__(self, title, content):
#         self.title = title
#         self.content = content

class WomenSerializer(serializers.ModelSerializer):
   class Meta:
      model = Women
      fields = '__all__'

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