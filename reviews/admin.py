from django.contrib import admin

# Register your models here.
from . import models as reviews_models


@admin.register(reviews_models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'content')
    list_filter = ('category',)


admin.site.register(reviews_models.Category)
admin.site.register(reviews_models.Company)
admin.site.register(reviews_models.ProductSize)
admin.site.register(reviews_models.ProductSite)
admin.site.register(reviews_models.Comment)
admin.site.register(reviews_models.Image)

admin.site.site_header = "Product Review Admin"
