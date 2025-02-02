from django.db import models
from django.utils.translation import gettext_lazy as _


# ============================================================= >> Product FILE
class ProductFile(models.Model):
    product = models.ForeignKey('products.Product', default=None,
                                on_delete=models.DO_NOTHING,
                                verbose_name=_("Product"))
    name = models.CharField(max_length=255,
                            verbose_name=_("Name"))
    short_description = models.CharField(max_length=255,
                                         verbose_name=_("Short description"))
    file = models.FileField(default=None, upload_to='products/files/',
                            verbose_name=_("File"))
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, null=True,
                                   verbose_name=_("Updated"))
    for_customer = models.BooleanField(default=True,
                                       verbose_name=_("For customers"))

    def __str__(self):
        return (f"{self.product.title}")

    def get_product_title(self):
        return self.product.title
    get_product_title.short_description = _("Product")

