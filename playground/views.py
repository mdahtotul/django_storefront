from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q, F
from django.http import HttpResponse
from store.models import Product, OrderItem, Order


def page_init(req):
    return HttpResponse(
        """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0" />
                <title>Playground</title>
            </head>
            <body>
                <h2><u>DJANGO PLAYGROUND</u></h2>
                <p>🚀 You're at the django playground.</p>
            </body>
            </html>
        """
    )


def all_query_set(req):
    query_set = Product.objects.all()

    for product in query_set:
        print(product)

    return render(req, "hello.html", {"name": "Arif"})


def get_product(req):
    try:
        product = Product.objects.get(pk=0)

    except ObjectDoesNotExist:
        pass
        # return HttpResponse("Product not found")

    return render(req, "hello.html", {"name": "Arif"})


def filter_product(req):
    try:
        # unit price greater than 20 using lookup
        # product = Product.objects.filter(unit_price__gt=20)

        # unit price range from 20 to 30
        # query_set = Product.objects.filter(unit_price__range=(20, 30))

        # string contains sensitive
        # query_set = Product.objects.filter(title__contains="coffee")

        # string contains insensitive
        # query_set = Product.objects.filter(title__icontains="coffee")

        query_set = Product.objects.filter(last_update__year=2020)

        return render(req, "hello.html", {"name": "Arif", "products": list(query_set)})

    except ObjectDoesNotExist:
        pass

    return render(req, "hello.html", {"name": "Arif"})


def complex_filter_product(req):
    # Products: inventory < 10 and unit_price < 20
    query_set_and = Product.objects.filter(inventory__lt=10, unit_price__lt=20)

    # Products: inventory < 10 or unit_price < 20
    query_set_or = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

    # //// Using F object we can reference a field value in the database
    # Products: reference unit_price with inventory
    query_set_f_obj = Product.objects.filter(inventory=F("unit_price"))

    # Products: reference collection.id with inventory
    query_set = Product.objects.filter(inventory=F("collection__id"))

    return render(req, "hello.html", {"name": "Arif", "products": list(query_set)})


def sorting_product(req):
    # lexically ascending sort
    query_set = Product.objects.order_by("title")

    # lexically descending sort
    query_set = Product.objects.order_by("-title")

    # unit_price ASC and lexically descending sort
    query_set = Product.objects.order_by("unit_price", "-title")

    # unit_price ASC and lexically descending sort
    query_set = Product.objects.filter(collection__id=1).order_by("unit_price")

    return render(req, "hello.html", {"name": "Arif", "products": list(query_set)})


def limiting_products(req):
    # getting first 5 products
    query_set_first_5 = Product.objects.all()[:5]
    # getting second 7 products
    query_set = Product.objects.all()[5:10]

    return render(req, "hello.html", {"name": "Arif", "products": list(query_set)})


def selecting_fields(req):
    # select only id, title of products and title of collection
    query_set = Product.objects.values("id", "title", "collection__title")
    # select products that have been ordered and sort them by title
    query_set = Product.objects.filter(
        id__in=OrderItem.objects.values("product__id").distinct()
    ).order_by("title")

    return render(
        req,
        "hello.html",
        {
            "name": "Arif",
            "reason": "Distinct ordered products",
            "products": list(query_set),
        },
    )


def deferring_fields(req):
    # be careful when using only() - if if you don't include the field that is showing on the template, it will provide a lot of extra queries

    query_set = Product.objects.only("id", "title", "unit_price")

    # be careful when using defer() - if if you include the field that is showing on the template, it will provide a lot of extra queries
    query_set = Product.objects.defer("description")

    return render(
        req,
        "hello.html",
        {
            "name": "Arif",
            "reason": "Distinct ordered products",
            "products": list(query_set),
        },
    )


def selecting_related_objects(req):
    # select_related() - when the other end of the relationship has 1 instance like Product has 1 Collection
    query_set = Product.objects.select_related("collection").all()

    # prefetch_related() - when the other end of the relationship has many instances like Collection has many Products
    query_set = Product.objects.prefetch_related("promotions").all()

    query_set = (
        Product.objects.prefetch_related("promotions")
        .select_related("collection")
        .all()
    )

    # last 5 orders with their customer and items (incl product)
    query_set = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set__product")
        .order_by("-placed_at")[:5]
    )
    return render(
        req,
        "hello.html",
        {
            "name": "Arif",
            "reason": "Distinct ordered products",
            "products": list(query_set),
        },
    )


def render_store_html(req):
    return render(req, "store.html", {"name": "core"})
