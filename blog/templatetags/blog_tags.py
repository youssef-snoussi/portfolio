import markdown

from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post


register = template.Library()


# Simple tag

@register.simple_tag
def total_posts():
    return Post.published.count()

# Inclusion tag: gets included in a template only

@register.inclusion_tag('blog/post/latest_posts.html')
def latest_posts(count=3):
    latest_posts = Post.published.order_by('-published_at')[:count]
    return {
        'latest_posts': latest_posts,
    }

# tag that returns a queryset

@register.simple_tag
def most_commented_posts(count=3):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by(
        '-total_comments'
    )[:count]


# a filter that format text to Markdown

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
