from django import forms

from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('name', 'email','body')

class PostForm(forms.ModelForm):
    image_url = forms.URLField(required=False, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Paste image link here...'}))
    slug = forms.SlugField(required=False, widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'url-slug-example'}))

    class Meta:
        model = Post
        fields = ('category', 'title', 'slug', 'intro', 'body', 'image', 'status')
        widgets = {
            'intro': forms.Textarea(attrs={'class': 'textarea', 'rows': 3, 'placeholder': 'A short summary of your article...'}),
            'title': forms.TextInput(attrs={'class': 'input is-medium', 'placeholder': 'Article Title'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if not image and not image_url:
            # It's okay to have no image if model allows blank=True, which it does.
            pass
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_url = self.cleaned_data.get('image_url')
        
        if image_url and not instance.image:
            import requests
            from django.core.files.base import ContentFile
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    filename = image_url.split("/")[-1]
                    if '?' in filename:
                        filename = filename.split('?')[0]
                    if not filename:
                        filename = 'image_from_url.jpg'
                    
                    instance.image.save(filename, ContentFile(response.content), save=False)
            except Exception as e:
                # Log error or ignore
                pass
        
        if commit:
            instance.save()
        return instance
        