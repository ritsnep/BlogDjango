from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from .forms import CommentForm
from .models import Post,Category

def detail(request, category_slug, slug):
    post=get_object_or_404(Post, slug=slug, status=Post.ACTIVE)

    if request.method == 'POST':
        form =CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.save()

            return redirect ('post_detail', post.category.slug, slug=slug)
    else:
        form = CommentForm()
    
    # Get related posts from the same category (excluding current post)
    related_posts = post.category.posts.filter(status=Post.ACTIVE).exclude(id=post.id)[:3]
    
    # Calculate read time (roughly 200 words per minute)
    word_count = len(post.body.split())
    read_time = max(1, word_count // 200)

    return render(request,'blog/detail.html',{
        'post':post,
        'form':form,
        'related_posts':related_posts,
        'read_time':read_time,
        'category':post.category
    })

def category(request, slug):
    category=get_object_or_404(Category, slug=slug)
    posts=category.posts.filter(status=Post.ACTIVE)
    return render(request,'blog/category.html',{'category':category, 'posts':posts})

def all_latest_articles(request):
    """Display all latest articles with pagination"""
    articles = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'blog/all_articles.html', {
        'posts': posts,
        'total_count': articles.count(),
        'section_title': 'Latest from Search Engine Land'
    })

def all_trending_articles(request):
    """Display all trending articles (by comment count) with pagination"""
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
        'section_title': 'Trending from Search Engine Land'
    })

def all_recent_articles(request):
    """Display all recent articles with pagination"""
    articles = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    paginator = Paginator(articles, 15)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    return render(request, 'blog/all_articles.html', {
        'posts': posts,
        'total_count': articles.count(),
        'section_title': 'Recent from Search Engine Land'
    })

from django.contrib.auth.models import User

def search(request):
    query=request.GET.get('query','')
    posts=Post.objects.filter(status=Post.ACTIVE).filter(Q(title__icontains=query) | Q(intro__icontains=query) |  Q(body__icontains=query))
    return render(request,'blog/search.html',{'posts':posts,'query':query})

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
