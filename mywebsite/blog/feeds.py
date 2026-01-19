from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Atom1Feed
from .models import Post

class LatestPostsFeed(Feed):
    title = "Search Signal Room - Latest Articles"
    link = "/feed/"
    description = "Latest digital marketing, SEO, and PPC insights from Search Signal Room."

    def items(self):
        return Post.objects.filter(status=Post.ACTIVE).order_by('-created_at')[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.intro

    def item_link(self, item):
        return reverse('post_detail', args=[item.category.slug, item.slug])
    
    def item_pubdate(self, item):
        return item.created_at
    
    def item_author_name(self, item):
        return item.author.get_full_name() or item.author.username

class LatestPostsAtomFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description
