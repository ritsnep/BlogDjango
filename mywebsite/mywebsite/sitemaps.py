from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from blog.models import Category,Post

class CategorySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    
    def items(self):
        return Category.objects.all()

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    
    def items(self):
        return Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')
    
    def lastmod(self, obj):
        return obj.created_at

from core.models import UserProfile

class UserSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5
    
    def items(self):
        return UserProfile.objects.exclude(role='Admin')
        
    def location(self, obj):
        return f'/author/{obj.user.username}/'

class StaticSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return ['frontpage', 'about', 'meet_the_team']

    def location(self, item):
        return reverse(item)
    