from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


def page_init(request):
    try:
        product = Product.objects.get(pk=0)

        # query_set = Product.objects.all()

        # for product in query_set:
        #     print(product)
    except ObjectDoesNotExist:
        pass
        # return HttpResponse("Product not found")

    return render(request, "hello.html", {"name": "Arif"})


def render_store_html(req):
    return render(req, "store.html", {"name": "core"})
