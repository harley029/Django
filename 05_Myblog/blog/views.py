from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from taggit.models import Tag

from blog.models import Post
from blog.forms import EmailPostForm, CommentForm, SearchForm


class PostListView(ListView):
    model = Post
    template_name = "blog/post/list.html"
    context_object_name = "posts"
    paginate_by = 3  # Кількість постів на сторінку

    def get_queryset(self):
        tag_slug = self.kwargs.get("tag_slug")
        queryset = Post.published.all()
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_slug = self.kwargs.get("tag_slug")
        if tag_slug:
            context["tag"] = get_object_or_404(Tag, slug=tag_slug)
        else:
            context["tag"] = None
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post/detail.html"
    context_object_name = "post"

    def get_object(self):
        year = self.kwargs.get("year")
        month = self.kwargs.get("month")
        day = self.kwargs.get("day")
        slug = self.kwargs.get("post")
        return get_object_or_404(
            Post,
            status=Post.Status.PUBLISHED,
            slug=slug,
            publish__year=year,
            publish__month=month,
            publish__day=day,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        # Активні коментарі
        comments = post.comments.filter(active=True)

        # Форма для додавання коментаря
        form = CommentForm()

        # Пошук схожих постів за тегами
        post_tags_ids = post.tags.values_list("id", flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(
            id=post.id
        )
        similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
            "-same_tags", "-publish"
        )[:4]

        context["comments"] = comments
        context["form"] = form
        context["similar_posts"] = similar_posts
        return context


class PostShareView(FormView):
    template_name = "blog/post/share.html"
    form_class = EmailPostForm

    def dispatch(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(
            Post, id=kwargs["post_id"], status=Post.Status.PUBLISHED
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Якщо форма валидна, отправляем email
        cd = form.cleaned_data
        post_url = self.request.build_absolute_uri(
            self.post_instance.get_absolute_url()
        )
        subject = f"{cd['name']} ({cd['email']}) recommends you read {self.post_instance.title}"
        message = f"Read {self.post_instance.title} at {post_url}\n\n{cd['name']}'s comments: {cd['comments']}"
        send_mail(subject, message, from_email=None, recipient_list=[cd["to"]])
        return self.render_to_response(self.get_context_data(form=form, sent=True))

    def get_context_data(self, **kwargs):
        # Добавляем объект поста в контекст
        context = super().get_context_data(**kwargs)
        context["post"] = self.post_instance
        return context


class PostCommentView(FormView):
    template_name = "blog/post/comment.html"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        # Отримуємо пост, до якого додається коментар
        self.post_instance = get_object_or_404(
            Post, id=kwargs["post_id"], status=Post.Status.PUBLISHED
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Якщо форма валідна, створюємо новий коментар без збереження в базі
        comment = form.save(commit=False)
        # Прив'язуємо коментар до поста
        comment.post = self.post_instance
        # Зберігаємо коментар в базі даних
        comment.save()

        # Повертаємо контекст з постом і коментарем
        return self.render_to_response(
            self.get_context_data(form=form, comment=comment)
        )

    def get_context_data(self, **kwargs):
        # Додаємо пост і форму в контекст
        context = super().get_context_data(**kwargs)
        context["post"] = self.post_instance
        context["comment"] = kwargs.get("comment")
        return context


class PostSearchView(FormView):
    template_name = "blog/post/search.html"
    form_class = SearchForm

    def get(self, request):
        # Якщо натиснута кнопка "Cancel", перенаправляємо користувача на список постів без валідації
        if "cancel" in request.GET:
            return redirect("blog:post_list")  # Перенаправлення на список постів

        # Якщо натиснута кнопка "Search", обробляємо форму як зазвичай
        if "query" in request.GET:
            form = self.form_class(request.GET)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.render_to_response(
                self.get_context_data(form=self.form_class())
            )

    def form_valid(self, form):
        # Отримуємо запит із форми після валідації
        query = form.cleaned_data["query"]
        # Створюємо пошукові вектори для заголовку та тіла поста з вагами
        search_vector = SearchVector(
            "title", weight="A", config="russian"
        ) + SearchVector("body", weight="B", config="russian")
        # Створюємо пошуковий запит
        search_query = SearchQuery(query, config="russian")
        # Виконуємо пошук і сортуємо результати за релевантністю
        results = (
            Post.published.annotate(
                search=search_vector, rank=SearchRank(search_vector, search_query)
            )
            .filter(rank__gte=0.3)
            .order_by("-rank")
        )
        # Повертаємо відповідь із результатами пошуку
        return self.render_to_response(
            self.get_context_data(form=form, query=query, results=results)
        )

    def get_context_data(self, **kwargs):
        # Додаємо пошуковий запит та результати в контекст
        context = super().get_context_data(**kwargs)
        context["query"] = kwargs.get("query", None)
        context["results"] = kwargs.get("results", [])
        return context


# ----------------- function views --------------------------------
def post_list(request, tag_slug=None):
    # posts = Post.published.all() - was without pagination

    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)  # Pagination with 3 posts per page
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    # List of similar posts
    post_tags_ids = post.tags.values_list("id", flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    # Get similar posts with same tags and sort by publish date (most recent first) and same_tags (most similar first)
    similar_posts = similar_posts.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )[:4]
    return render(
        request,
        "blog/post/detail.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "similar_posts": similar_posts,
        },
    )


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if "query" in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data["query"]
            search_vector = SearchVector(
                "title", weight="A", config="russian"
            ) + SearchVector("body", weight="B", config="russian")
            search_query = SearchQuery(query, config="russian")
            # Используем SearchQuery для фильтрации результатов
            results = (
                Post.published.annotate(
                    search=search_vector, rank=SearchRank(search_vector, search_query)
                )
                .filter(rank__gte=0.3)
                .order_by("-rank")  # Сортировка по релевантности
            )
    return render(
        request,
        "blog/post/search.html",
        {"form": form, "query": query, "results": results},
    )
