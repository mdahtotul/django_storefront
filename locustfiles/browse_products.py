from locust import HttpUser, task, between
from random import randint

class WebsiteUser(HttpUser):
    wait_time = between(1,5)

    @task(2)
    def view_products(self):
        collection_id = randint(2, 6)
        self.client.get(f"/store/products/?collection_id={collection_id}", name="/store/products")

    @task(4)
    def view_product(self):
        product_id = randint(1, 1000)
        self.client.get(f"/store/products/{product_id}", name="/store/products/:id")

    
    @task(1)
    def add_to_cart(self):
        product_id = randint(1, 10)
        self.client.post(f"/store/carts/{self.cart_id}/items/",
                          name="/store/carts/items",
                          json={
                              "product_id": product_id,
                              "quantity": 1
                          }
                        )
        
    @task
    def say_hello(self):
        self.client.get("/playground/hello", name="/playground/hello")

    
    def on_start(self):
        response = self.client.post('/store/carts/')
        result = response.json()
        self.cart_id = result['id']


"""
Performance testing script (locust)

Core use cases for business logic:
1/ Browse products
2/ View product details
3/ Add product to cart
4/ Register, sign in, sign out
"""

"""
tips to improve performance:
# preload related objects
Product.objects.select_related().all()
Products.objects.prefetch_related().all()

# load only what you need
Product.objects.only('id', 'name', 'price').all()
Product.objects.defer('description').all()

# use values
Product.objects.values('id', 'name', 'price').all()
Product.objects.values_list('id', 'name', 'price').all()

# count properly
Product.objects.count()
len(Product.objects.all()) #Bad
Product.objects.all().count() #Bad


# bulk create/update
Product.objects.bulk_create([])
"""