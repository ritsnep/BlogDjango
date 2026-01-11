from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileForm

# Inline profile editor for User admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserProfileForm
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'

# Custom User admin including profile inline
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    
    def get_role(self, instance):
        try:
            return instance.userprofile.role
        except UserProfile.DoesNotExist:
            return None
    get_role.short_description = 'Role'

# Re-register User with customized admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
