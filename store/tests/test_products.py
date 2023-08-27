from decimal import Decimal
from typing import Collection
from rest_framework import status
import pytest
from model_bakery import baker
from store.models import Product, Collection
import json

@pytest.fixture
def create_product(api_client):
  def receive_instance(product):
    return api_client.post('/store/products/', product)
  return receive_instance

@pytest.mark.django_db
class TestCreateProduct:
  def test_if_user_is_anonymous_returns_401(self, api_client, create_product):
    # Arrange

    # Act
    response = create_product({'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, api_client, create_product):
    # Arrange
    authenticate(is_staff=False)
    # Act
    response = create_product({'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_data_is_invalid_returns_400(self, authenticate, api_client, create_product):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = create_product({'title': ''})
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None

  def test_if_data_is_valid_returns_201(self, authenticate, api_client, create_product):
    # Arrange
    authenticate(is_staff=True)
    collection = baker.make(Collection)
    instance = {
        "title": "test3",
        "slug": "test-3",
        "description": "",
        "unit_price": 15.63,
        "inventory": 4,
        "collection": collection.id
    }
    # Act
    response = create_product(instance)
    # Assert
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
class TestRetrieveProduct:
  def test_if_product_exists_returns_200(self, api_client):
    # Arrange
    product = baker.make(Product)
    # Act
    response = api_client.get(f'/store/products/{product.id}/')
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        'id': product.id,
        'title': product.title,
        'slug': product.slug,
        'description': product.description,
        'inventory': product.inventory,
        'unit_price': product.unit_price,
        'price_with_tax': product.unit_price * Decimal(1.15),
        'collection': product.collection.id,
        'images': []
    }


@pytest.fixture
def update_product(api_client):
  def receive_instance(instance, is_valid_data=True):
    collection = baker.make(Collection)
    product = baker.make(Product, collection=collection)
    updated_data = {
        "title": instance['title'],
        "slug": "updated-slug",
        "description": "Updated description",
        "unit_price": 19.99,
        "inventory": 8,
        "collection": collection.id
    }
    if not is_valid_data:
      updated_data = {}

    return api_client.put(f'/store/products/{product.id}/', updated_data)
  return receive_instance

@pytest.mark.django_db
class TestUpdateProduct:
  def test_if_user_is_anonymous_returns_401(self, api_client, update_product):
    # Arrange
    updated_data = {
        "title": "Updated Title",
    }
    # Act
    response = update_product(updated_data)
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, api_client, update_product):
    # Arrange
    authenticate(is_staff=False)
    updated_data = {
        "title": "Updated Title",
    }
    # Act
    response = update_product(updated_data)
    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_product_does_not_exist_returns_404(self, authenticate, api_client, update_product):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = api_client.put('/store/products/1/', {})
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

  def test_if_data_is_invalid_returns_400(self, authenticate, api_client, update_product):
    # Arrange
    authenticate(is_staff=True)
    updated_data = {
        "title": 1,
    }
    # Act
    response = update_product(updated_data, is_valid_data=False)
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None

  def test_if_data_is_valid_returns_200(self, authenticate, api_client, update_product):
    # Arrange
    authenticate(is_staff=True)
    updated_data = {
        "title": "Updated Title",
        # "slug": "updated-slug",
        # "description": "Updated description",
        # "unit_price": 19.99,
        # "inventory": 8,
        # "collection": collection.id
    }
    # Act
    response = update_product(updated_data)
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'Updated Title'


@pytest.fixture
def delete_product(api_client):
  def receive_instance():
    collection = baker.make(Collection)
    product = baker.make(Product, collection=collection)
    return api_client.delete(f'/store/products/{product.id}/')
  return receive_instance

@pytest.mark.django_db
class TestDeleteProduct:
  def test_if_user_is_anonymous_returns_401(self, api_client, delete_product):
    # Arrange

    # Act
    response = delete_product()
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, api_client, delete_product):
    # Arrange
    authenticate(is_staff=False)
    # Act
    response = delete_product()
    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_product_does_not_exist_returns_404(self, authenticate, api_client, delete_product):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = api_client.delete('/store/products/1/')
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

  def test_if_product_exists_returns_204(self, authenticate, api_client, delete_product):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = delete_product()
    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT

  