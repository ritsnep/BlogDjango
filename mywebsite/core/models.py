from django.db import models
from django.contrib.auth.models import User

# User profile for authors and team members
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('Author', 'Author'),
        ('Editor', 'Editor'),
        ('Writer', 'Writer'),
        ('SEO Expert', 'SEO Expert'),
        ('Admin', 'Admin'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='Writer')
    bio = models.TextField(blank=True, null=True, help_text="Bio for author page and post footer")
    profile_image = models.ImageField(upload_to='uploads/authors/', blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    
    def get_image_url(self):
        # Handle both local files and external URLs
        if self.profile_image:
            image_str = str(self.profile_image)
            if image_str.startswith('http'):
                return image_str
            return self.profile_image.url
        return "https://ui-avatars.com/api/?name=" + self.user.username + "&background=random"

    def get_contact_email(self):
        # Returns profile email or falls back to user email
        return self.email or getattr(self.user, 'email', '')
