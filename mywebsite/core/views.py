from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q, Count
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.views.decorators.http import condition
from django.template.loader import render_to_string
from django.urls import reverse

from blog.models import Post, Category
from mywebsite.sitemaps import CategorySitemap, PostSitemap, UserSitemap, StaticSitemap
import xml.dom.minidom
from datetime import datetime
from django.utils import timezone

def frontpage(request):
    # Get active posts ordered by creation date (newest first)
    active_posts = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    # Featured article - the most recent post
    featured_post = active_posts.first()
    
    # Latest news - next 3 most recent posts after featured
    latest_posts = active_posts[1:4]
    
    # Recent articles - positions 4 onwards, limit to 6
    recent_posts = active_posts.exclude(id=featured_post.id if featured_post else None).exclude(
        id__in=[p.id for p in latest_posts if latest_posts.exists()]
    )[:6]
    
    # Trending articles - posts with most comments
    trending_posts = Post.objects.filter(
        status=Post.ACTIVE
    ).exclude(
        id=featured_post.id if featured_post else None
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-comment_count', '-created_at')[:6]

    # Fetch specific categories for the "Top" sections
    seo_cat = Category.objects.filter(title__iexact='SEO').first()
    ppc_cat = Category.objects.filter(title__iexact='PPC').first()
    dm_cat = Category.objects.filter(title__iexact='Digital Marketing').first()
    
    # Fallback if specific categories don't exist
    if not seo_cat or not ppc_cat or not dm_cat:
        cats_with_posts = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
        if not seo_cat and cats_with_posts.count() > 0:
            seo_cat = cats_with_posts[0]
        if not ppc_cat and cats_with_posts.count() > 1:
            ppc_cat = cats_with_posts[1]
        if not dm_cat and cats_with_posts.count() > 0:
            dm_cat = cats_with_posts[0]

    seo_posts = Post.objects.filter(category=seo_cat, status=Post.ACTIVE)[:3] if seo_cat else []
    ppc_posts = Post.objects.filter(category=ppc_cat, status=Post.ACTIVE)[:3] if ppc_cat else []
    dm_posts = Post.objects.filter(category=dm_cat, status=Post.ACTIVE)[:6] if dm_cat else []

    # Categories for the interactive Guides section (limit to top 2 for clarity/design)
    guides_categories_list = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count')[:2]
    
    # Pre-fetch posts for these specific top 2 categories to avoid N+1 in template
    # We'll store them in a list of dicts for easy access
    guides_data = []
    for cat in guides_categories_list:
        guides_data.append({
            'category': cat,
            'posts': cat.posts.filter(status=Post.ACTIVE).order_by('-created_at')[:6]
        })
    
    context = {
        'featured_post': featured_post,
        'latest_posts': latest_posts,
        'recent_posts': recent_posts,
        'trending_posts': trending_posts,
        'seo_cat': seo_cat,
        'ppc_cat': ppc_cat,
        'dm_cat': dm_cat,
        'seo_posts': seo_posts,
        'ppc_posts': ppc_posts,
        'dm_posts': dm_posts,
        'guides_data': guides_data,
        'posts': active_posts 
    }
    
    return render(request, 'core/frontpage.html', context)

def about(request):
    return render(request, 'core/about.html')

def robot_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri(reverse('django.contrib.sitemaps.views.sitemap'))}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

def custom_404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'core/404.html', status=404)

from .models import UserProfile

def test_404(request):
    """Test view to preview 404 page during development"""
    return render(request, 'core/404.html')

def meet_the_team(request):
    team_members = UserProfile.objects.all().select_related('user')
    
    role_groups = [
        ('SEO Expert', team_members.filter(role='SEO Expert')),
        ('Author', team_members.filter(role='Author')),
        ('Editor', team_members.filter(role='Editor')),
        ('Writer', team_members.filter(role='Writer')),
    ]
    
    context = {
        'role_groups': role_groups
    }
    return render(request, 'core/meet_the_team.html', context)


def sitemap_html(request):
    """Display sitemap as a user-friendly HTML page"""
    categories = Category.objects.all().order_by('title')
    posts = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    context = {
        'categories': categories,
        'posts': posts,
        'total_urls': len(categories) + len(posts)
    }
    return render(request, 'core/sitemap.html', context)


def sitemap_xml(request):
    """Enhanced sitemap.xml with XSLT styling"""
    sitemaps_dict = {
        'category': CategorySitemap,
        'post': PostSitemap,
        'user': UserSitemap,
        'static': StaticSitemap
    }
    
    # Get the raw XML sitemap response from Django's sitemap view
    response = sitemap_view(request, sitemaps=sitemaps_dict)
    
    # Access rendered_content to trigger rendering of TemplateResponse
    content = response.rendered_content
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    
    # Insert XSLT processing instruction after XML declaration
    if content.startswith('<?xml'):
        end_of_declaration = content.find('?>')
        if end_of_declaration != -1:
            xslt_pi = f'<?xml-stylesheet type="text/xsl" href="/static/sitemap.xsl"?>'
            content = content[:end_of_declaration + 2] + '\n' + xslt_pi + content[end_of_declaration + 2:]
    
    # Return a new HttpResponse with proper content type
    return HttpResponse(content, content_type='application/xml; charset=utf-8')



