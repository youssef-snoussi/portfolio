from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

from core.models import BaseModel

# Create your models here.

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                    .filter(status=Post.Status.PUBLISHED)

class Post(BaseModel):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(max_length=255,
                            unique_for_date="published_at",
                            verbose_name="Slug")
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name="Author")
    body = models.TextField(verbose_name="Body")
    published_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT,
                              verbose_name="Status")

    objects = models.Manager()
    published = PublishedManager()

    # Tags Manager
    tags = TaggableManager()

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]

    def __str__(self):
        return f"{self.title} by {self.author or ''}"

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.published_at.year,
                             self.published_at.month,
                             self.published_at.day,
                             self.slug
                           ])

class Comment(BaseModel):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments",
                             verbose_name="Post"
    )
    name = models.CharField(max_length=80, verbose_name="Name")
    email = models.EmailField(verbose_name="E-mail")
    body = models.TextField(verbose_name="Body")
    active = models.BooleanField(default=True, verbose_name="Active?")

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
