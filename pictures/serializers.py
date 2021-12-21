import io
from pathlib import Path

import requests
from django.core import files
from django.core.files.uploadedfile import TemporaryUploadedFile, UploadedFile
from requests import request
from rest_framework import serializers

from config import settings
from .models import Figure
from django.core.files.base import ContentFile
from PIL import Image
from urllib.parse import urlparse


class FigureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Figure
        fields = "__all__"
        read_only_fields = ['width', 'height']

    def validate(self, raw_data):
        url = raw_data.get('url')
        picture = raw_data.get('picture')
        if url and picture:
            raise serializers.ValidationError('picture or url not together')
        if not url and not picture:
            raise serializers.ValidationError('picture or url must exist')

        return raw_data


    def create(self, validated_data):
        name = validated_data.get('name')
        url = validated_data.get('url')
        width = validated_data.get('width')

        print(validated_data)
        instance = super().create(validated_data)
        if url:
            picture_from_url_response = requests.get(url, stream=True)
            if picture_from_url_response.status_code != 200:
                raise serializers.ValidationError('picture not found')
            instance.picture.save(Path(url).name, files.File(io.BytesIO(picture_from_url_response.content)))
            o = urlparse(url)
            ind = o.path.rfind('/')
            name_from_url = o.path[ind+1:]
            instance.name = name_from_url
            im = Image.open(instance.picture)
            width, height = im.size
            instance.width = width
            instance.height = height

            instance.save()
            return instance

            # f = open(name_from_url, 'wb')
            #
            # f.write(picture_from_url_response.content)
            # f.close()

            # width, height = im.size
            # instance.width = width
            # instance.height = height
            # instance.name = name_from_url
            # instance.save()
            # return instance
        else:

            im = Image.open(instance.picture)
            width, height = im.size
            instance.width = width
            instance.height = height
            instance.name = name
            instance.save()
            return instance

    def detail_picture(self, instance_id):
        idx = instance_id.get('id')
        return idx.instance

class FigureResizeSerializer(serializers.Serializer):
    width = serializers.IntegerField(min_value=1, required=False )
    height = serializers.IntegerField(min_value=1, required=False)

    def validate(self, raw_data):
        width = raw_data.get('width')
        height = raw_data.get('height')
        if not (width and height or height or width):
            raise serializers.ValidationError('not data for resize')
        return raw_data


    # def resize_picture(self, instance_id, data):
    #     new_width = data.get('width')
    #     new_height = data.get('height')
    #     if new_width and new_height or new_width or new_height:
    #         idx = instance_id.get('id')
    #         instance = super().save()
    #         im = Image.open(instance.picture)
    #         new_width, new_height = im.size
    #         instance.width = new_width
    #         instance.height = new_width
    #         instance.parent_picture = idx
    #         instance.save()
    #         return instance



