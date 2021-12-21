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


