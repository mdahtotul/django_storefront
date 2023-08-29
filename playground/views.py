from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, mail_admins, mail_managers, BadHeaderError, EmailMessage
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.cache import cache_page
from django.db import transaction, connection
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.aggregates import Count, Sum, Max, Min, Avg
from django.db.models.functions import Concat
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage
from playground.tasks import notify_users
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem
from rest_framework.views import APIView
import requests
import logging

logger = logging.getLogger(__name__) #playground.views

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

def render_store_html(req):
    return render(req, "store.html", {"name": "core"})


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
            "reason": "Selecting or Prefetching related fields",
            "products": list(query_set),
        },
    )


def aggregate_objects(req):
    # filter product then aggregating results
    result = Product.objects.filter(collection__id=1).aggregate(
        count=Count("id"), min_price=Min("unit_price"), max_price=Max("unit_price")
    )

    # total number of products
    result = Product.objects.aggregate(
        count=Count("id"), min_price=Min("unit_price"), max_price=Max("unit_price")
    )

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Aggregate Queries", "result": result},
    )


def annotating_objects(req):
    # adding new column name 'is_new'
    result = Customer.objects.annotate(is_new=Value(True))

    # adding new column name 'new_id'
    result = Customer.objects.annotate(new_id=F("id"))

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Aggregate Queries", "result": list(result)},
    )


def using_db_functions(req):
    # CONCAT
    query_set = Customer.objects.annotate(
        full_name=Func(F("first_name"), Value(" "), F("last_name"), function="CONCAT")
    )

    query_set = Customer.objects.annotate(
        full_name=Concat("first_name", Value(" "), "last_name")
    )

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Database function", "result": list(query_set)},
    )


def grouping_data(req):
    query_set = Customer.objects.annotate(orders_count=Count("order"))

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Database function", "result": list(query_set)},
    )


def expression_wrappers(req):
    discounted_price = ExpressionWrapper(
        F("unit_price") * 0.8, output_field=DecimalField()
    )
    query_set = Product.objects.annotate(discount_price=discounted_price)

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Database function", "result": list(query_set)},
    )


def generic_relationship(req):
    content_type = ContentType.objects.get_for_model(Product)

    query_set = TaggedItem.objects.select_related("tag").filter(
        content_type=content_type, object_id=1
    )

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Database function", "result": list(query_set)},
    )


def custom_managers(req):
    # custom manager is created in tags\models.py
    query_set = TaggedItem.objects.get_tags_for(Product, 1)

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Database function", "result": list(query_set)},
    )


def create_collection(req):
    collection = Collection()
    collection.title = "Video Games"
    collection.featured_product = Product(pk=1)
    collection.save()

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Collection created", "id": collection.id},
    )


def update_collection(req):
    # Don't update like this
    # collection = Collection(pk=11)
    # collection.title = "Games"
    # collection.featured_product = None
    # collection.save()

    # update like this
    collection = Collection.objects.get(pk=11)
    collection.featured_product = None
    collection.save()

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Collection updated", "id": collection.id},
    )


def delete_collection(req):
    collection = Collection(pk=11)
    # single object delete
    collection.delete()

    # multiple object delete
    Collection.objects.filter(id__gt=10).delete()

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Collection updated", "id": collection.id},
    )


def transaction_query(req):
    # .... other code that is outside of transaction wrapper

    # transaction.atomic() - if any error occurs, during all operations it will rollback to previous state
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Collection updated", "id": ""},
    )


def executing_sql_query(req):
    # approach 1
    query_set = Product.objects.raw("SELECT * FROM store_product")
    # approach 2
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM store_product")
        query_set = cursor.fetchall()

    return render(
        req,
        "hello.html",
        {"name": "Arif", "reason": "Raw SQL query", "result": list(query_set)},
    )


def normal_emailing(request):
    try:
        send_mail('subject', 'message', 'info@arifbuy.com', ['bob@arifbuy.com'])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return render(request, 'hello.html', {'name': 'Arif'})


def admin_emailing(request):
    try:
        mail_admins('subject', 'message', html_message='<h1>message</h1>')
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return render(request, 'hello.html', {'name': 'Arif'})


def send_file_email(request):
    try:
        message = EmailMessage('Check attach file', 'Check that file', 'arifulht@gmail.com', ['charlie@arifbuy.com'])
        message.attach_file('playground/static/images/2.png')
        message.send()
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return render(request, 'hello.html', {'name': 'Arif'})


def send_template_email(request):
    try:
        message = BaseEmailMessage(
            template_name='emails/test.html',
            context={
                'subject': 'check template email',
                'to_person': 'Shuvo',
                'from_person': 'Arif',
            },
        )
        message.send(['shuvo629@gmail.com'])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')
    return render(request, 'hello.html', {'name': 'Arif'})

def executing_task_using_celery(request):
    notify_users.delay('Hello')
    return render(request, 'hello.html', {'name': 'Arif'})


"""
@cache_page(5 * 60)
def check_low_level_cache(req):
    response = requests.get("https://httpbin.org/delay/2")
    data = response.json()

    return render(req, 'hello.html', {'name': data})
"""


class CheckLowLevelCache(APIView):
    @method_decorator(cache_page(5 * 60))
    def get(self, req):
        response = requests.get("https://httpbin.org/delay/2")
        data = response.json()

        return render(req, 'hello.html', {'name': data})

class UsingLogger(APIView):
    def get(self, req):
        try:
            logger.info("Calling httpbin")
            response = requests.get("https://httpbin.org/delay/1")
            data = response.json()
            logger.info("Response received")
        except requests.ConnectionError as e:
            logger.critical('httpbin is offline')

        return render(req, 'hello.html', {'name': data})
    

