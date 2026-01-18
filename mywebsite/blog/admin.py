from django.contrib import admin
from django import forms

from .models import Post,Category,Comment

class CommentItemInline(admin.TabularInline):
    model = Comment
    raw_id_fields=['post']
    

class PostAdminForm(forms.ModelForm):
    image_url = forms.URLField(required=False, help_text="Paste an image URL to download and set as Featured Image")

    class Meta:
        model = Post
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_url = self.cleaned_data.get('image_url')
        if image_url and not instance.image:
             try:
                import requests
                from django.core.files.base import ContentFile
                response = requests.get(image_url)
                if response.status_code == 200:
                    filename = image_url.split("/")[-1].split("?")[0] or 'downloaded_image.jpg'
                    instance.image.save(filename, ContentFile(response.content), save=False)
             except Exception:
                 pass
        if commit:
            instance.save()
        return instance

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    search_fields=['title','intro','body' ]
    list_display=['title','slug','category','author','created_at','status']
    list_filter=['category','author','created_at','status']
    
    # Show image_url field in admin
    fieldsets = (
        (None, {
            'fields': ('category', 'author', 'title', 'slug', 'status')
        }),
        ('Content', {
            'fields': ('intro', 'body', 'image', 'image_url')
        }),
        ('Dates', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    inlines=[CommentItemInline]
    prepopulated_fields={'slug':('title',)}

class CategoryAdmin(admin.ModelAdmin):
    search_fields=['title']
    list_display=['title']
    prepopulated_fields={'slug':('title',)}

class CommentAdmin(admin.ModelAdmin):
    list_display=['name','post','created_at']
admin.site.register(Post,PostAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Comment,CommentAdmin)