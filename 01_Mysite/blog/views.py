from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


from taggit.models import Tag


from blog.models import Post, Comment


def post_list(request, tag_slug=None):
    # posts = Post.published.all()
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger: # Если page_number не целое число, то выдать первую страницу
        posts = paginator.page(1)
    except EmptyPage:        # Если page_number находится вне диапазона, то выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'posts': posts, 'tag': tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status="PB",
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True) 
    # Форма для комментирования пользователями
    form = CommentForm()
    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True) 
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form, 'similar_posts': similar_posts},
    )

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="PB")
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'python_web22@meta.ua', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status="PB")
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST) 
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию 
        comment.post = post
        # Сохранить комментарий в базе данных 
        comment.save()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})

def post_search(request): 
    form = SearchForm() 
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET) 
        if form.is_valid():
            query = form.cleaned_data['query'] 
            search_vector = SearchVector('title', 'body') 
            search_query = SearchQuery(query)
            results = (
                Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query))
                .filter(search=search_query)
                .order_by("-rank")
            )
    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )

class PostListView(ListView): 
    """ Альтернативное представление списка постов """
    # queryset = Post.published.all() 
    queryset = Post.objects.all() 
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
