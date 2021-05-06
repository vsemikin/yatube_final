from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, Comment, Follow

User = get_user_model()

PER_PAGE = 10


def index(request):
    """The function returns the model objects to the page template,
    sorting them in descending date order and
    limiting the number of objects displayed to 10 per page."""
    post_list = Post.objects.all()
    paginator = Paginator(post_list, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'posts/index.html', {
            'page': page,
            'is_post_view': False
        }
    )


def group_posts(request, slug):
    """The function returns model objects of a certain template group
    to the page, sorts them in descending order of date, and
    limits the number of objects displayed on the page to 10."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.groups.all()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'group.html', {
            'group': group,
            'page': page,
            'is_post_view': False
        }
    )


@login_required
def new_post(request):
    """The function passes the form to the template and
    saves the data from the form to the database."""
    form = PostForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(
            request, 'posts/new.html', {'form': form, 'is_new': True}
        )
    else:
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')


def profile(request, username):
    """The function passes data to the user profile page template."""
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'posts/profile.html', {
            'author': user,
            'page': page,
            'is_post_view': False
        }
    )


def post_view(request, username, post_id):
    """The function passes data to the page template of a specific post."""
    post = get_object_or_404(Post, id=post_id, author__username=username)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    if request.method == 'GET' or not form.is_valid():
        return render(
            request, 'posts/post.html', {
                'author': post.author,
                'post': post,
                'form': form,
                'comments': comments,
                'is_post_view': True
            }
        )
    else:
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
        return redirect('post_view', username, post.id)


@login_required
def post_edit(request, username, post_id):
    """The function transfers data to the post edit page template
    and saves the changes."""
    post = get_object_or_404(Post, id=post_id, author__username=username)
    if post.author != request.user:
        return redirect('post_view', username, post.id)
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if request.method == 'GET' or not form.is_valid():
        return render(
            request,
            'posts/new.html',
            {'form': form, 'post': post, 'is_new': False}
        )
    else:
        form.save()
        return redirect('post_view', username, post.id)


def page_not_found(request, exception):
    """The function returns the template of the 404 error page
    when it occurs."""
    return render(
        request,
        'misc/404.html',
        {'path': request.path},
        status=404
    )


def server_error(request):
    """The function returns the template of the 500 error page
    when it occurs."""
    return render(request, 'misc/500.html', status=500)


def add_comment(request, username, post_id, comment_id):
    """The function transfers data to the template of the comment edit page
    and saves the changes.."""
    post = get_object_or_404(Post, id=post_id, author__username=username)
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.author != request.user:
        return redirect('post_view', username, post.id)
    form = CommentForm(request.POST or None, instance=comment)
    if request.method == 'GET' or not form.is_valid():
        return render(
            request,
            'posts/new.html',
            {'form': form, 'is_new': False}
        )
    else:
        form.save()
        return redirect('post_view', username, post.id)


@login_required
def follow_index(request):
    """The function returns the posts of the authors that
    the current user is following."""
    authors = request.user.following.all()
    posts = authors.posts.all()
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {'page': page})


@login_required
def profile_follow(request, username):
    """."""
    Follow.user = request.user
    


@login_required
def profile_unfollow(request, username):
    """."""
