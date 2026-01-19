from django.urls import path

from . import views
from .feeds import LatestPostsFeed, LatestPostsAtomFeed


urlpatterns=[
    path('feed/', LatestPostsFeed(), name='rss_feed'),
    path('feed/atom/', LatestPostsAtomFeed(), name='atom_feed'),
    path('create-post/', views.create_post, name='create_post'),
    path('post/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('my-posts/trash/<slug:slug>/', views.move_to_trash, name='move_to_trash'),
    path('my-posts/restore/<slug:slug>/', views.restore_post, name='restore_post'),
    path('my-posts/delete/<slug:slug>/', views.delete_post_permanently, name='delete_post_permanently'),
    path('my-posts/comments/delete/<int:pk>/', views.delete_comment, name='delete_comment'),
    path('search/',views.search,name='search'),
    path('all-latest/',views.all_latest_articles,name='all_latest'),
    path('all-trending/',views.all_trending_articles,name='all_trending'),
    path('all-recent/',views.all_recent_articles,name='all_recent'),
    path('author/<str:username>/', views.author_detail, name='author_detail'),
    path('<slug:category_slug>/<slug:slug>/',views.detail, name='post_detail'),

    path('<slug:slug>/',views.category, name='category_detail'),
]  