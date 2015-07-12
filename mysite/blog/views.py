from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Comment
from .forms import PostForm, CommentForm, ImportPostForm
from bs4 import BeautifulSoup, Comment
import urllib.request

def add_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/accounts/login/', pk = user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'registration/add_user.html', {'form': form})

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def list_my_post(request):
    posts = Post.objects.filter(author=request.user.pk).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        if post.author_id == request.user.pk:
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('blog.views.post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True, author=request.user.pk).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=pk)
        if post.author_id == request.user.pk:
            post.publish()
    return redirect('blog.views.post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author_id == request.user.pk:
        post.delete()
    return redirect('blog.views.post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)

def import_post(request):
    return render(request, 'blog/import_post.html', {})

@csrf_exempt
def soup_load_post(request):

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        try:
            url=request.GET['url']
            imgs = []
            req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
            with urllib.request.urlopen(req) as response:
                page = response.read()

            soup = BeautifulSoup(page)

            # get title
            title = soup("title")

            # get text
            text = soup.get_text()

            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))

            cont = 0
            cont_aux = 0
            text_aux = ""

            for chunk in chunks:
                if chunk == "":
                    if cont < cont_aux:
                        text = text_aux
                        cont = cont_aux
                    text_aux = ""
                    cont_aux = 0
                else:
                    text_aux += chunk
                    cont_aux += len(chunk)

            post = Post(title=title, text=text)
            form = PostForm(instance=post)

            return render(request, 'blog/post_edit.html', {'form': form})

        except Exception as e:
            return render(request, 'blog/import_post.html', {})
