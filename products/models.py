from django.db import models
from datetime import datetime, date
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from core.libs.core_libs import (get_headshot_image, get_image_format,
                                 get_coordinates)


def product_dir_path(instance, filename):
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    return (f'products/{filename}')


# ============================================================= >> PRODUCT TYPE
class ProductType(models.Model):
    """ProductTypes designate basic appartment, maisonette, loft, houses, etc.
    """

    name = models.CharField(max_length=100, blank=False, null=False,
                            unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    def get_nr_products(self):
        return 5


PRODUCT_CHOICE = {
    (_("IS"), _("In Stock")),
    (_("OS"), _("Out of Stock")),
}


# ================================================================== >> PRODUCT
class Product(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT,
                                     verbose_name=_("Product type"))
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    description = models.TextField(blank=True,
                                   verbose_name=_("Description"))
    price = models.DecimalField(max_digits=20, decimal_places=2,
                                verbose_name=_("Price"))
    image = models.ImageField(upload_to=product_dir_path,
                              verbose_name=_("Image"))
    product_is = models.CharField(max_length=5, choices=PRODUCT_CHOICE,
                                   default="IS", verbose_name=_("Product is"))
    protected = models.BooleanField(default=False,
                                    verbose_name=_("Monument Protected"))
    is_published = models.BooleanField(default=True, verbose_name=_("Online"))
    free_from = models.DateField(default=datetime.now, blank=True,
                                 verbose_name=_("Free from"))
    created = models.DateTimeField(auto_now_add=True, null=True,
                                   verbose_name=_("Created"))
    updated = models.DateTimeField(auto_now=True, null=True,
                                   verbose_name=_("Updated"))

    def __str__(self):
        return self.title

    def free_date(self):
        if self.free_from <= date.today():
            return _("Immediatly")
        else:
            return self.free_from

    def get_price(self):
        return f"{self.price}€"
    get_price.short_description = _("Price")

    def get_image(self):
        return get_image_format(self.image)

    get_image.short_description = _('Image')

    def headshot_image(self):
        return get_headshot_image(self.image)

    headshot_image.short_description = _('Preview')

    def get_images(self):
        '''returns nr of inline images'''
        return self.productimage_set.count() + 1 if self.image else \
            self.productimage_set.count()

    get_images.short_description = _('# Images')

    def get_nr_files(self):
        '''returns nr of inline files'''
        return self.productfile_set.count()
    get_nr_files.short_description = _('# Files')


# ============================================================ >> PRODUCT IMAGE
class ProductImage(models.Model):
    product = models.ForeignKey(Product, default=None,
                                on_delete=models.DO_NOTHING,
                                verbose_name=_("Product"))
    image = models.ImageField(default=None, upload_to=product_dir_path,
                              null=True, blank=True,
                              verbose_name=_("Image"))
    short_description = models.CharField(max_length=255,
                                         verbose_name=_("Short description"))
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name=_("Created"))

    def __str__(self):
        return (f"{self.product.title}")

    def get_image(self):
        return get_image_format(self.image)

    get_image.short_description = _("Image")

    def headshot_image(self):
        return get_headshot_image(self.image)

    headshot_image.short_description = _("Preview")

    def get_product_title(self):
        return self.product.title

    get_product_title.short_description = _("Product")


# ============================================================= >> PRODUCT FILE
class ProductToCustomer(models.Model):
    product = models.ForeignKey(Product, default=None,
                                on_delete=models.DO_NOTHING)
