from django.urls import path
from . import views

urlpatterns = [
    path("", views.page_init),
    path("hello/", views.render_store_html),
]
