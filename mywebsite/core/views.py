from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Count
from django.contrib.sitemaps.views import sitemap as sitemap_view
from django.urls import reverse
from blog.models import Post, Category
from mywebsite.sitemaps import CategorySitemap, PostSitemap, UserSitemap, StaticSitemap
from .models import UserProfile

# Home page view with featured, latest, and trending posts
def frontpage(request):
    active_posts = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    featured_post = active_posts.first()
    latest_posts = active_posts[1:4]
    
    # Exclude featured and latest from recent posts
    recent_posts = active_posts.exclude(id=featured_post.id if featured_post else None).exclude(
        id__in=[p.id for p in latest_posts if latest_posts.exists()]
    )[:6]
    
    # Trending posts sorted by comment count
    trending_posts = Post.objects.filter(
        status=Post.ACTIVE
    ).exclude(
        id=featured_post.id if featured_post else None
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-comment_count', '-created_at')[:6]

    # Specific categories for top sections
    seo_cat = Category.objects.filter(title__iexact='SEO').first()
    ppc_cat = Category.objects.filter(title__iexact='PPC').first()
    dm_cat = Category.objects.filter(title__iexact='Digital Marketing').first()
    
    # Fallback to any available categories
    if not seo_cat or not ppc_cat or not dm_cat:
        cats_with_posts = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
        if not seo_cat and cats_with_posts.count() > 0: seo_cat = cats_with_posts[0]
        if not ppc_cat and cats_with_posts.count() > 1: ppc_cat = cats_with_posts[1]
        if not dm_cat and cats_with_posts.count() > 0: dm_cat = cats_with_posts[0]

    seo_posts = Post.objects.filter(category=seo_cat, status=Post.ACTIVE)[:3] if seo_cat else []
    ppc_posts = Post.objects.filter(category=ppc_cat, status=Post.ACTIVE)[:3] if ppc_cat else []
    dm_posts = Post.objects.filter(category=dm_cat, status=Post.ACTIVE)[:6] if dm_cat else []

    # Prepare data for the guides section
    guides_categories_list = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0).order_by('-post_count')[:2]
    guides_data = []
    for cat in guides_categories_list:
        guides_data.append({
            'category': cat,
            'posts': cat.posts.filter(status=Post.ACTIVE).order_by('-created_at')[:6]
        })
    
    return render(request, 'core/frontpage.html', {
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
    })

# About page
def about(request):
    return render(request, 'core/about.html')

# Robot.txt for SEO
def robot_txt(request):
    lines = [
        "User-agent: *",
        "Disallow: /admin/",
        f"Sitemap: {request.build_absolute_uri(reverse('django.contrib.sitemaps.views.sitemap'))}"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

# Custom 404 error page
def custom_404(request, exception):
    return render(request, 'core/404.html', status=404)

# Preview 404 page for testing
def test_404(request):
    return render(request, 'core/404.html')

# Team page showing all user profiles
def meet_the_team(request):
    team_members = UserProfile.objects.all().select_related('user')
    role_groups = [
        ('SEO Expert', team_members.filter(role='SEO Expert')),
        ('Author', team_members.filter(role='Author')),
        ('Editor', team_members.filter(role='Editor')),
        ('Writer', team_members.filter(role='Writer')),
    ]
    return render(request, 'core/meet_the_team.html', {'role_groups': role_groups})

# HTML sitemap for users
def sitemap_html(request):
    categories = Category.objects.all().order_by('title')
    posts = Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    return render(request, 'core/sitemap.html', {
        'categories': categories,
        'posts': posts,
        'total_urls': len(categories) + len(posts)
    })

# XML sitemap with XSLT styling
def sitemap_xml(request):
    sitemaps_dict = {
        'category': CategorySitemap,
        'post': PostSitemap,
        'user': UserSitemap,
        'static': StaticSitemap
    }
    
    response = sitemap_view(request, sitemaps=sitemaps_dict)
    content = response.rendered_content
    if isinstance(content, bytes):
        content = content.decode('utf-8')
    
    # Add XSLT stylesheet reference
    if content.startswith('<?xml'):
        end_of_declaration = content.find('?>')
        if end_of_declaration != -1:
            xslt_pi = f'<?xml-stylesheet type="text/xsl" href="/static/sitemap.xsl"?>'
            content = content[:end_of_declaration + 2] + '\n' + xslt_pi + content[end_of_declaration + 2:]
    
    return HttpResponse(content, content_type='application/xml; charset=utf-8')



