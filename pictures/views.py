import io

from PIL import Image
from django.core.files.base import ContentFile
from rest_framework import viewsets
from .models import Figure
from .serializers import FigureSerializer, FigureResizeSerializer
from rest_framework.decorators import action
from rest_framework.response import Response



class FigureViewSet(viewsets.ModelViewSet):
    queryset = Figure.objects.all()
    serializer_class = FigureSerializer


    @action(methods=['POST'], detail=True)
    def resize(self, request, pk):
        instance = self.get_object()

        input_serializer = FigureResizeSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        im = Image.open(instance.picture)

        new_width = input_serializer.validated_data.get('width', instance.width)
        new_height = input_serializer.validated_data.get('height', instance.width)

        new_im = im.resize((new_width, new_height))
        new_width, new_height = new_im.size
        new_instance = Figure(parent_picture_id=pk, height=new_height, width=new_width, name=instance.name)
        f = io.BytesIO()
        new_im.save(f, format='png')
        s = f.getvalue()
        extension = instance.picture.name.split('.')[-1]
        new_instance.picture.save(instance.name+'.'+extension, ContentFile(s))

        new_instance.save()
        serializer = self.get_serializer(new_instance)

        return Response(serializer.data)

        #вставка stackoverflow.com
        # buffer = io.BytesIO()
        # new_im.save(fp=buffer, format='JPEG')
        # return ContentFile(buffer.getvalue())

        # assuming your Model instance is called `instance`
        # image_field = instance.image_field
        # img_name = 'my_image.jpg'
        # img_path = settings.MEDIA_ROOT + img_name
        #
        # pillow_image = resize_image(
        #     image_field,
        #     width=IMAGE_WIDTH,
        #     height=IMAGE_HEIGHT,
        #     name=img_path)

    #
    #
    #
    #     new_instance = Figure(height=new_height, width=new_width, name=instance.name)
    #     instance.picture.save(
    #         instance.name,
    #         new_im
    #     )
    #     new_instance.save()
    #     #instance.parent_picture = pk
    #
    #     serializer = self.get_serializer(new_instance)
    #     return Response(serializer.data)
    #
    #     im = Image.open(instance.picture)
    #     width, height = im.size
    #     instance.width = width
    #     instance.height = height
    #     instance.name = name
    #     instance.save()
    #     return instance
    #
    #     # сохранение обьекта pillow в file_field модели Django
    #
    #
