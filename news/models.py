# from django.core.urlresolvers import reverse
from cms.models import CMSPlugin
from django.db import models

# Create your models here.
from django.urls import reverse
from djangocms_text_ckeditor.fields import HTMLField


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название новости')
    content = HTMLField(null=True, blank=True, verbose_name='Содержание')
    added = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Добавлена')
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name='Изменена')
    image = models.ImageField(null=True, blank=True, verbose_name='Картинка')
    status = models.BooleanField(default=True, verbose_name='Активен')

    objects = PostManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-added"]
        verbose_name = 'Новость'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        # return reverse('news_list', kwargs={'pk': self.id})
        return "/news/{id}".format(id=self.id)

class PostPlugin(CMSPlugin):
    latest_articles = models.IntegerField(
        default=6,
        # help_text=_('The maximum number of latest articles to display.')
    )
    # post = models.ForeignKey(Post)

    def __str__(self):
        return str(self.latest_articles)

    def get_posts(self):
        posts = Post.objects.all()[:self.latest_articles]
        return posts
