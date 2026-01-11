from django import forms
from .models import UserProfile
import requests
from django.core.files.base import ContentFile
from urllib.parse import urlparse

# Form for UserProfile with image download capability
class UserProfileForm(forms.ModelForm):
    image_url = forms.URLField(
        required=False, 
        help_text="Optional: Enter an image URL to download as your profile image."
    )

    class Meta:
        model = UserProfile
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        image_url = cleaned_data.get('image_url')

        if image_url:
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                
                # Validate content type
                content_type = response.headers.get('content-type', '')
                if not content_type.startswith('image'):
                     self.add_error('image_url', "URL does not point to a valid image.")
                     return cleaned_data

                # Extract filename or guess extension
                parsed_url = urlparse(image_url)
                file_name = parsed_url.path.split('/')[-1]
                if not file_name or '.' not in file_name:
                    ext = 'jpg'
                    if 'png' in content_type: ext = 'png'
                    elif 'gif' in content_type: ext = 'gif'
                    elif 'jpeg' in content_type: ext = 'jpg'
                    elif 'webp' in content_type: ext = 'webp'
                    file_name = f"downloaded_image.{ext}"
                
                self.downloaded_image_content = ContentFile(response.content)
                self.downloaded_image_name = file_name
                
            except Exception as e:
                self.add_error('image_url', f"Failed to download image: {str(e)}")
        
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Save downloaded image if present
        if hasattr(self, 'downloaded_image_content') and self.downloaded_image_content:
            instance.profile_image.save(self.downloaded_image_name, self.downloaded_image_content, save=False)
        
        if commit:
            instance.save()
        return instance
