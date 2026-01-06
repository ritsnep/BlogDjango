"""
URL configuration for mywebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import sitemaps
from django.contrib.sitemaps.views import sitemap
from django.contrib import admin
from django.urls import include, path


from .sitemaps import CategorySitemap, PostSitemap
from core.views import frontpage, about, robot_txt, test_404, meet_the_team, sitemap_html, sitemap_xml




sitemaps= {'category':  CategorySitemap, 'post':PostSitemap}

urlpatterns = [
    path('robots.txt', robot_txt, name='robots_txt'),
    path('sitemap.xml', sitemap_xml, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap/', sitemap_html, name='sitemap_html'),
    path('admin/', admin.site.urls),
    path('',frontpage, name='frontpage'),
    path('about/',about, name='about'),
    path('team/', meet_the_team, name='meet_the_team'),
    path('test-404/', test_404, name='test_404'),  # Test URL for 404 page
    path('ckeditor5/', include('django_ckeditor_5.urls')),
    path('', include('blog.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Custom error handlers
handler404 = 'core.views.custom_404'

