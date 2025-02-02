from django.contrib import admin
from django.contrib.admin.widgets import AdminFileWidget
from documents.models import ProductFile
from django.utils.html import format_html
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

pdf_img_path = settings.STATIC_URL + 'img/pdf.png'


class AdminImageWidget(AdminFileWidget):
    '''Generates Image Preview of StackedInline class'''

    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            file_url = value.url
            file_name = str(value)
            output.append(f'<a href="{file_url}" target="_blank">'
                          f' <img src="{pdf_img_path}" alt={file_name}" '
                          f'width="50" height="50"  style="object-fit:'
                          f' cover;"/></a> {_("Placeholder")} ')
        output.append(super(AdminFileWidget, self).render(name, value, attrs))
        return format_html(u''.join(output))


class InlineProductFileAdmin(admin.StackedInline):
    model = ProductFile
    formfield_overrides = {models.FileField: {'widget': AdminImageWidget}}


@admin.register(ProductFile)
class ProductFileAdmin(admin.ModelAdmin):
    search_fields = ['product__title', 'product__realtor__first_name',
                     'product__realtor__last_name']
    autocomplete_fields = ['product']
    readonly_fields = ('updated', 'created')
    list_display = ('product', 'name', 'short_description', 'for_customer',
                    'created')
