from rest_framework import status
import pytest
from model_bakery import baker
from store.models import Product

@pytest.fixture
def create_product(api_client):
  def receive_instance(product):
    return api_client.post('/store/products/', product)
  return receive_instance