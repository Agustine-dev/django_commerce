from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.admin.widgets import AdminFileWidget
from .models import *
from documents.admin import InlineProductFileAdmin

def set_online(modeladmin, request, queryset):
    queryset.update(is_published=True)


def set_offline(modeladmin, request, queryset):
    queryset.update(is_published=False)

class AdminImageWidget(AdminFileWidget):
    '''Generates Image Preview of StackedInline class'''

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(f'<a href="{image_url}" target="_blank">'
                          f' <img src="{image_url}" alt={file_name}" '
                          f'width="150" height="150"  style="object-fit:'
                          f' cover;"/></a> {_("Placeholder")} ')
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return format_html(u''.join(output))


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage
    formfield_overrides = {models.ImageField: {'widget': AdminImageWidget}}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin, InlineProductFileAdmin]
    search_fields = ('title',
                     'description','price',
                     'product_type__name')
    autocomplete_fields = ['product_type']
    list_display = ('title', 'is_published', 'product_type','get_price', 'free_from', 'product_is','get_nr_files', 'get_images', 'get_image')
    list_display_links = ('title',)
    list_filter = ('product_is', 'is_published')
    list_editable = ('is_published',)
    actions = [set_online, set_offline]
    readonly_fields = ('created', 'updated', 'headshot_image')
    list_per_page = 25
    save_as = True


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id', 'name')
    list_editable = ('name',)
    actions = [set_online, set_offline]
    readonly_fields = ('created', 'updated')


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    search_fields = ['product__title',]
    autocomplete_fields = ['product']
    list_editable = ('short_description',)
    readonly_fields = ('headshot_image', 'created')
    list_display = ('get_product_title', 'short_description', 'get_image')
