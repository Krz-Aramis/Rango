from django.contrib import admin
from rango.models import Category, Page

# Class to customise the Admin interface
# It ensures that the slug field is automatically populated
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug':('name',)}

# Update the registration of our models with our custom interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page)
