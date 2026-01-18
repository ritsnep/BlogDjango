
from django.urls import path


from . import views


urlpatterns=[
    path('create-post/', views.create_post, name='create_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    path('search/',views.search,name='search'),
    path('all-latest/',views.all_latest_articles,name='all_latest'),
    path('all-trending/',views.all_trending_articles,name='all_trending'),
    path('all-recent/',views.all_recent_articles,name='all_recent'),
    path('author/<str:username>/', views.author_detail, name='author_detail'),
    path('<slug:category_slug>/<slug:slug>/',views.detail, name='post_detail'),

    path('<slug:slug>/',views.category, name='category_detail'),
]  