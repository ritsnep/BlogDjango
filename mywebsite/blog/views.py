from django.db.models import Q, Count
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from core.models import UserProfile
from core.forms import PublicUserProfileForm

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user

            # Handle Draft/Publish Actions
            action = request.POST.get('action')
            if action == 'draft':
                post.status = Post.DRAFT
            else:
                post.status = Post.ACTIVE
            
            # Use provided slug or generate from title
            if form.cleaned_data.get('slug'):
                post.slug = form.cleaned_data['slug']
            else:
                post.slug = slugify(post.title)
            
            # Ensure unique slug
            original_slug = post.slug
            count = 1
            while Post.objects.filter(slug=post.slug).exists():
                post.slug = f"{original_slug}-{count}"
                count += 1
            
            post.save()
            form.save() # Handles m2m and image_url logic from Form.save() method
            
            # Process new tags (create any that don't exist)
            process_new_tags(request, post)
            
            return redirect('post_detail', category_slug=post.category.slug, slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/create_post.html', {'form': form, 'is_edit': False})

def process_new_tags(request, post):
    """Process and create new tags from the form submission"""
    from .models import Tag
    
    # Get all selected tag values
    tag_values = request.POST.getlist('tags')
    tag_objects = []
    
    for tag_value in tag_values:
        # Try to get existing tag by slug
        try:
            tag = Tag.objects.get(slug=tag_value)
            tag_objects.append(tag)
        except Tag.DoesNotExist:
            # This is a new tag - create it
            # The tag_value is the slug, we need to get the name from data attribute
            # For new tags, the slug is generated from the name
            # We'll use the slug to create a readable name
            tag_name = tag_value.replace('-', ' ').title()
            tag = Tag.objects.create(name=tag_name, slug=tag_value)
            tag_objects.append(tag)
    
    # Set the tags for the post
    post.tags.set(tag_objects)

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            
            # Update status if action button clicked
            action = request.POST.get('action')
            if action:
                if action == 'draft':
                    post.status = Post.DRAFT
                elif action == 'publish':
                    post.status = Post.ACTIVE
            
            post.save()
            form.save()
            
            # Process new tags (create any that don't exist)
            process_new_tags(request, post)
            
            return redirect('my_posts')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/create_post.html', {
        'form': form,
        'is_edit': True,
        'post': post
    })

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

    # Get categories for sidebar
    categories = Category.objects.all()[:3]

    return render(request,'blog/detail.html',{
        'post':post,
        'form':form,
        'related_posts':related_posts,
        'read_time':read_time,
        'category':post.category,
        'categories': categories
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
    
    # Get distinct categories that this author has written about
    author_categories = Category.objects.filter(
        posts__author=author,
        posts__status=Post.ACTIVE
    ).distinct().order_by('title')
    
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_posts = paginator.get_page(page_number)
    
    return render(request, 'blog/author_detail.html', {
        'author': author,
        'posts': page_posts,
        'categories': author_categories
    })

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    active_posts = posts.filter(status=Post.ACTIVE)
    draft_posts = posts.filter(status=Post.DRAFT)
    trash_posts = posts.filter(status=Post.TRASH)
    
    comments = Comment.objects.filter(post__author=request.user).order_by('-created_at')
    
    # Profile Logic
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = PublicUserProfileForm(request.POST, request.FILES, instance=user_profile)
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email_user', user.email)
        user.save()
        
        if profile_form.is_valid():
            profile_form.save()
            return redirect('my_posts')
    else:
        profile_form = PublicUserProfileForm(instance=user_profile)

    return render(request, 'blog/my_posts.html', {
        'active_posts': active_posts,
        'draft_posts': draft_posts,
        'trash_posts': trash_posts,
        'comments': comments,
        'profile_form': profile_form
    })

@login_required
def move_to_trash(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    post.status = Post.TRASH
    post.save()
    return redirect('my_posts')

@login_required
def restore_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    post.status = Post.DRAFT
    post.save()
    return redirect('my_posts')

@login_required
def delete_post_permanently(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    post.delete()
    return redirect('my_posts')

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk, post__author=request.user)
    comment.delete()
    return redirect('my_posts')
