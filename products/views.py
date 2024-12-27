from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView
from django.db.models import Q
from decimal import Decimal
from django.utils.html import format_html

from .models import Product, ProductType
from core.models import State


# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    object_list = Product.objects.order_by('-created').filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object_list  # change this
        # Showcase Section Info
        context['title'] = _("Browse our products")
        # SEO
        context['page_title'] = _("Browse Listed Products")
        context['page_description'] = _("Fashion Designing", "Latest Trends")
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['price'] = self.object.price
        # SEO
        context['page_title'] = self.object.title
        context['page_description'] = _("Product manager."
                                        "Description and attribute listing of "
                                        "a specific object you are "
                                        "interested in.")
        return context


def search(request):
    res = Product.objects.order_by('-created')

    keywords = request.GET.get('keywords', "")
    product_type = request.GET.get('product_type', 0)
    max_price = request.GET.get('price', Decimal(10000000))

    if not max_price:
        max_price = 1000000000

    queryset_list = res.filter(
        (Q(description__icontains=keywords) |
         Q(title__icontains=keywords)),
        price__lte=max_price,
    )

    try:
        if isinstance(int(product_type), int):
            queryset_list = queryset_list.filter(product_type=product_type)
    except Exception:
        pass

    context = {
        'states': State.objects.all(),
        'list_types': ProductType.objects.all(),
        'products': queryset_list,
        'values': request.GET
    }

    return render(request, 'search.html', context)

