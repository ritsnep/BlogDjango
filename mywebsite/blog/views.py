from django.db.models import Q, Count
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .forms import CommentForm
from .models import Post,Category

# View post detail and handle comments
def detail(request, category_slug, slug):
    post=get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form =CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()

            return redirect('post_detail', category_slug=post.category.slug, slug=slug)
    else:
        form = CommentForm()
    
    # Get related posts from the same category
    related_posts = post.category.posts.filter(status=Post.ACTIVE).exclude(id=post.id)[:3]
    
    # Calculate estimated read time
    word_count = len(post.body.split())
    read_time = max(1, word_count // 200)

    return render(request,'blog/detail.html',{
        'post':post,
        'form':form,
        'related_posts':related_posts,
        'read_time':read_time,
        'category':post.category
    })

# View posts by category
def category(request, slug):
    category=get_object_or_404(Category, slug=slug)
    posts=category.posts.filter(status=Post.ACTIVE)
    return render(request,'blog/category.html',{'category':category, 'posts':posts})

# View all latest articles with pagination
def all_latest_articles(request):
    articles = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'blog/all_articles.html', {
        'posts': posts,
        'total_count': articles.count(),
        'section_title': f"Latest from {settings.SITE_NAME}"
    })

# View all trending articles based on comment count
def all_trending_articles(request):
    articles = Post.objects.filter(
        status=Post.ACTIVE
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-comment_count', '-created_at')
    
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'blog/all_articles.html', {
        'posts': posts,
        'total_count': articles.count(),
        'section_title': f"Trending from {settings.SITE_NAME}"
    })

# View all recent articles
def all_recent_articles(request):
    articles = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'blog/all_articles.html', {
        'posts': posts,
        'total_count': articles.count(),
        'section_title': f"Recent from {settings.SITE_NAME}"
    })

# Search for posts by title or content
def search(request):
    query=request.GET.get('query','')
    posts=Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) |  Q(body__icontains=query))
    return render(request,'blog/search.html',{'posts':posts,'query':query})

# View posts by a specific author
def author_detail(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.filter(status=Post.ACTIVE).order_by('-created_at')
    
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    
    return render(request, 'blog/author_detail.html', {
        'author': author,
        'posts': page_posts
    })
