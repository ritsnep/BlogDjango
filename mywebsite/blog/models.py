from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

# Categories for blog posts
class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('title',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug

# Tags for blog posts
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/tag/%s/' % self.slug

# Blog post model
class Post(models.Model):
    ACTIVE = 'active'
    DRAFT = 'draft'
    TRASH = 'trash'
    
    STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft'),
        (TRASH, 'Trash')
    )

    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    intro = models.TextField()
    body = CKEditor5Field('Text', config_name='extends')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
    
    def get_image_url(self):
        # Handle both local files and external URLs
        if self.image:
            image_str = str(self.image)
            if image_str.startswith('http'):
                return image_str
            return self.image.url
        return None

# User comments on posts
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
