from django.views.generic import TemplateView
from django.core.paginator import InvalidPage
from django.contrib import messages
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404, redirect

from oscar.core.loading import get_class, get_model

get_product_search_handler_class = get_class(
    'catalogue.search_handlers', 'get_product_search_handler_class')


class CatalogueView(TemplateView):
    """
    Browse all products in the catalogue
    """
    context_object_name = "products"
    template_name = 'catalogue/browse.html'

    def get(self, request, *args, **kwargs):
        if request.GET.get('items', None):
            settings.OSCAR_PRODUCTS_PER_PAGE = request.GET['items']
        try:
            self.search_handler = self.get_search_handler(
                self.request.GET, request.get_full_path(), [])
        except InvalidPage:
            # Redirect to page one.
            messages.error(request, _('The given page number was invalid.'))
            return redirect('catalogue:index')
        return super(CatalogueView, self).get(request, *args, **kwargs)

    def get_search_handler(self, *args, **kwargs):
        return get_product_search_handler_class()(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = {}
        ctx['summary'] = _("All products")
        search_context = self.search_handler.get_search_context_data(
            self.context_object_name, self.request)
        ctx.update(search_context)
        ctx['OSCAR_PRODUCTS_PER_PAGE'] = int(settings.OSCAR_PRODUCTS_PER_PAGE)
        ctx['ITEM_IN_PAGE_LIST'] = [10, 20, 30, 40]
        return ctx