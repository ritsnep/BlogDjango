from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    class Meta:
        ordering=('title',)
        verbose_name_plural='Categories'

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return '/%s/' % self.slug

class Post(models.Model):
    ACTIVE='active'

    DRAFT='draft'
    STATUS_CHOICES=(
        (ACTIVE, 'Active'),
        (DRAFT,'Draft')
    )
    category=models.ForeignKey(Category,related_name='posts',on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)

    slug = models.SlugField()
    intro=models.TextField()
    body=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default=ACTIVE)
    image=models.ImageField(upload_to='uploads/',blank=True, null=True)
    
    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)
    
    def get_image_url(self):
        """Returns the image URL, handling both local files and external URLs"""
        if self.image:
            image_str = str(self.image)
            # Check if it's an external URL (starts with http)
            if image_str.startswith('http'):
                return image_str
            # Otherwise, it's a local file
            return self.image.url
        return None

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name= models.CharField(max_length=255)
    email = models.EmailField()
    body= models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name