from .models import Category

# Makes categories available globally to all templates
def menu_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}
