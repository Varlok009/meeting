from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Group, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page, 'paginator': paginator})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, 'page': page, 'paginator': paginator})


@login_required()
def new_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('index')
    context = {'text': 'Добавить'}
    return render(request, 'new_post.html', {'form': form, 'context': context})


def profile(request, username):
    user_data = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author__username=username).order_by("-pub_date")
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 'profile.html', {
            "profile": user_data,
            'page': page,
            'paginator': paginator,
            'count_posts': len(post_list)
        }
    )


@login_required()
def post_view(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, id=post_id)
    comments = Comment.objects.filter(post=post)

    form = CommentForm(request.POST or None)
    return render(request, 'post.html', {'post': post, 'form': form, 'comments': comments})


@login_required()
def post_edit(request, username, post_id):
    if request.user.username != username:
        return redirect('post', username, post_id)
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post', username, post_id)
    context = {'text': 'Редактировать'}
    return render(request, 'new_post.html', {'form': form, 'context': context, 'post': post})


@login_required()
def add_comment(request, username, post_id):
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = get_object_or_404(Post, author__username=username, id=post_id)
        comment.save()
        return redirect('post', username, post_id)
    return render(request, 'post.html', {'post': post, 'form': form, 'comments': comments})
