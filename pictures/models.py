from django.db import models


class Figure(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to='site_media/', blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    parent_picture = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        return self.name

# Create your models here.
