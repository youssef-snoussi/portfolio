from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.db.models import Count
from django.views.decorators.http import require_POST
# from django.views.generic import ListView

from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm

# Create your views here.

# class PostListView(ListView):
#     """
#         This is an alternative to the function based view
#     """
#     queryset = Post.published.all()
#     context_object_name = 'posts'
#     paginate_by = 3
#     template_name = 'blog/post/list.html'



def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(
            Tag,
            slug=tag_slug
        )
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts,
                   'tag': tag
                  }
    )

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             slug=post,
                             published_at__year=year,
                             published_at__month=month,
                             published_at__day=day,
                             status=Post.Status.PUBLISHED
    )

    comments = post.comments.filter(active=True).order_by('-created_at')
    form = CommentForm()

    # Retreiving similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids
    ).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-published_at')[:3]

    return render(request,
                  'blog/post/detail.html',
                  {"post":post,
                   "comments": comments,
                   "form": form,
                   "similar_posts": similar_posts
                  }
    )

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read {post}"
            message = f"Read {post} at {post_url}\n\n {cd['name']}'s comment: {cd['comment']}"
            send_mail(subject, message, "your_account@gmail.com", [cd['to']])
            sent = True

    else:
         form = EmailPostForm()

    return render(request,
                  'blog/post/share.html',
                  {'post': post,
                   'form': form,
                   'sent': sent}
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,
                  'blog/post/detail.html#comment_parial',
                  {'post': post,
                   'form': form,
                   'comment': comment
                  }
    )


def search_post(request):
    search_term = request.POST.get('search')
    if len(search_term) == 0:
        posts = Post.published.none()
    else:
        posts = Post.published.filter(body__contains=search_term)
    return render(
        request,
        'blog/base.html#search_result',
        {'search_posts': posts}
    )


