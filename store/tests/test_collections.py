from rest_framework import status
import pytest
from model_bakery import baker
from store.models import Collection

@pytest.fixture
def create_collection(api_client):
  def receive_instance(collection):
    return api_client.post('/store/collections/', collection)
  return receive_instance

@pytest.mark.django_db
class TestCreateCollection:
  def test_if_user_is_anonymous_returns_401(self, api_client, create_collection):
    # Arrange

    # Act
    response = create_collection({'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


  def test_if_user_is_not_admin_returns_403(self, authenticate, api_client, create_collection):
    # Arrange
    authenticate(is_staff=False)
    # Act
    response = create_collection({'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN


  def test_if_data_is_invalid_returns_400(self, authenticate, api_client, create_collection):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = create_collection({'title': ''})
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None


  def test_if_data_is_valid_returns_201(self, authenticate, api_client, create_collection):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = create_collection({'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollection:
  def test_if_collection_exists_returns_200(self, api_client):
    # Arrange
    collection = baker.make(Collection)
    # Act
    response = api_client.get(f'/store/collections/{collection.id}/')
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
      'id': collection.id,
      'title': collection.title,
      'products_count': 0
    }

@pytest.mark.django_db
class TestUpdateCollection:
  def test_if_user_is_anonymous_returns_401(self, api_client):
    # Arrange
    collection = baker.make(Collection)
    # Act
    response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
    # Arrange
    authenticate(is_staff=False)
    collection = baker.make(Collection)
    # Act
    response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_collection_does_not_exist_returns_404(self, authenticate, api_client):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = api_client.put('/store/collections/1/', {'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

  def test_if_data_is_invalid_returns_400(self, authenticate, api_client):
    # Arrange
    authenticate(is_staff=True)
    collection = baker.make(Collection)
    # Act
    response = api_client.put(f'/store/collections/{collection.id}/', {'title': ''})
    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['title'] is not None

  def test_if_data_is_valid_returns_200(self, authenticate, api_client):
    # Arrange
    authenticate(is_staff=True)
    collection = baker.make(Collection)
    # Act
    response = api_client.put(f'/store/collections/{collection.id}/', {'title': 'a'})
    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.data['title'] == 'a'


@pytest.mark.django_db
class TestDeleteCollection:
  def test_if_user_is_anonymous_returns_401(self, api_client):
    # Arrange
    collection = baker.make(Collection)
    # Act
    response = api_client.delete(f'/store/collections/{collection.id}/')
    # Assert
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

  def test_if_user_is_not_admin_returns_403(self, authenticate, api_client):
    # Arrange
    authenticate(is_staff=False)
    collection = baker.make(Collection)
    # Act
    response = api_client.delete(f'/store/collections/{collection.id}/')
    # Assert
    assert response.status_code == status.HTTP_403_FORBIDDEN

  def test_if_collection_does_not_exist_returns_404(self, authenticate, api_client):
    # Arrange
    authenticate(is_staff=True)
    # Act
    response = api_client.delete('/store/collections/1/')
    # Assert
    assert response.status_code == status.HTTP_404_NOT_FOUND

  def test_if_collection_exists_returns_204(self, authenticate, api_client):
    # Arrange
    authenticate(is_staff=True)
    collection = baker.make(Collection)
    # Act
    response = api_client.delete(f'/store/collections/{collection.id}/')
    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Collection.objects.filter(id=collection.id).exists()