from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from blog.models import Category, Post
from core.models import UserProfile

# Category sitemap
class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    
    def items(self):
        return Category.objects.all()

# Blog post sitemap
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    def lastmod(self, obj):
        return obj.created_at

# Author sitemap
class UserSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    
    def items(self):
        return UserProfile.objects.exclude(role='Admin')
        
    def location(self, obj):
        return f'/author/{obj.user.username}/'

# Static pages sitemap
class StaticSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['frontpage', 'about', 'meet_the_team']

    def location(self, item):
        return reverse(item)
    