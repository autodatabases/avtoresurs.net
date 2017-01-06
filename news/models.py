from django.db import models

# Create your models here.
from django.urls import reverse


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название новости')
    content = models.TextField(null=True, blank=True, verbose_name='Содержание')
    added = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(null=True, blank=True)
    status = models.BooleanField(default=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-updated"]

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'pk': self.id})
