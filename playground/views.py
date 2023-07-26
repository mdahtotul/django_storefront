from django.shortcuts import render
from django.http import HttpResponse
from store.models import Product


def page_init(request):
    query_set = Product.objects.all()

    return render(request, "hello.html", {"name": "Arif"})


def render_store_html(req):
    return render(req, "store.html", {"name": "core"})
