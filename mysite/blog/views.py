from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import PostForm, CommentForm
from .models import Post, Image
from .bsoup import safe_html

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
    posts = Post.objects.order_by('created_date')
    return render(request, 'blog/home.html', {'posts': posts})

def list_my_post(request):
    posts = Post.objects.filter(author=request.user.pk).order_by('created_date')
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
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)

def import_post(request):
    return render(request, 'blog/import_post.html', {})

@csrf_exempt
def soup_load_post(request):
    try:
        url=request.GET['url']
        imgs = []
        req = urllib.request.Request(url, headers={'User-Agent' : "Magic Browser"})
        with urllib.request.urlopen(req) as response:
            page = response.read()

        soup = BeautifulSoup(page, "html.parser")
        title = soup("title")

        for img in soup.find_all('img'):
            if img['src'].find("http") == 0:
                imgs.append(img['src'])

        page = safe_html(page)

        soup = BeautifulSoup(page, "html.parser")

        # get text
        text = soup.get_text()

        post = Post(title=title, text=text, url=url)
        post.author = request.user
        post.save()

        for i in imgs:
            image = Image(post = post, url = i)
            image.save()

        return redirect('blog.views.post_detail', pk=post.pk)

    except Exception as e:
        return render(request, 'blog/import_post.html', {"msg": "Link está zoado!"})
