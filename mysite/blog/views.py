from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from .forms import PostForm, CommentForm
from .models import Post, Image, Tag
from .bsoup import safe_html

from bs4 import BeautifulSoup, Comment
import urllib.request

def home(request):
    posts = post_list()
    tags = ranking_of_tags()
    return render(request, 'blog/home.html', {'posts': posts, 'tags': tags})

def post_list():
    posts = Post.objects.order_by('-created_date')
    return posts

def ranking_of_tags():
    tags = Tag.objects.values('tag').annotate(Count('tag')).order_by('-tag__count')[:10]
    return tags

def post_list_by_tag(request, tag):
    post_resp = []
    if not str(tag) == "":
        tags = Tag.objects.filter(tag = "#"+tag)
        for i in tags:
            if not i.post in post_resp:
                post_resp.append(i.post)
    return render(request, 'blog/post_list.html', {'posts': post_resp, 'tag': '#'+tag})

def post_search(request):
    post_resp = []
    keyWord = request.GET['keyWord']
    tag = "Resultados da busca"
    querySet = Post.objects.filter(Q(title__icontains = keyWord) | Q(text__icontains = keyWord) |
        Q(url__icontains = keyWord)| Q(tags__tag__icontains = keyWord))\
        .order_by('created_date').distinct()
    return render(request, 'blog/post_list.html', {'posts': querySet, 'tag': ''+tag})


def add_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('/accounts/login/', pk = user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'registration/add_user.html', {'form': form})

@login_required
def list_my_post(request):
    posts = Post.objects.filter(author=request.user.pk).order_by('created_date')
    return render(request, 'blog/post_list.html', {'posts': posts, 'tag': 'Meus Posts'})

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
    return redirect('blog.views.list_my_post')

@login_required
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

@login_required
def import_post(request):
    return render(request, 'blog/import_post.html', {})

@login_required
def import_post_add_tag(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/import_post_add_tag.html', {'post': post})

@login_required
def post_add_tag(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":

        tags = request.POST['tag']

        current_tags = Tag.objects.filter(post=post)
        for i in current_tags:
            i.delete()

        for tag in tags.split(" "):
            if tag != "" and str(tag)[0] == "#":
                tag = Tag(post = post, tag = tag.split(" ")[0])
                tag.save()
    return render(request, 'blog/import_post_add_tag.html', {"msg": "Post Cadastrado com sucesso!", "post": post})

@csrf_exempt
@login_required
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

        return redirect('blog.views.import_post_add_tag', pk=post.pk)

    except Exception as e:
        return render(request, 'blog/import_post.html', {"msg": "Link está zoado!"})

