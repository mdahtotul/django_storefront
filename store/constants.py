PAYMENT_STATUS_PENDING = "P"
PAYMENT_STATUS_COMPLETE = "C"
PAYMENT_STATUS_FAILED = "F"

PAYMENT_STATUS_CHOICES = [
    (PAYMENT_STATUS_PENDING, "Pending"),
    (PAYMENT_STATUS_COMPLETE, "Complete"),
    (PAYMENT_STATUS_FAILED, "Failed"),
]

def get_all_domains(domain_name):
    all_domains = [
        {
            "name": "home",
            "endpoint": domain_name,
            "token": "",
            "req_type": "GET",
            "access_role": "Public"

        },
        {
            "name": "auth-users",
            "endpoint": f"{domain_name}/auth/users",
            "token": "",
            "req_type": "GET, POST",
            "access_role": "Admin, Public"
        },
        {
            "name": "create JWT token",
            "endpoint": f"{domain_name}/auth/jwt/create",
            "token": "",
            "req_type": "POST",
            "access_role": "Public"
        },
        {
            "name": "refresh JWT token",
            "endpoint": f"{domain_name}/auth/jwt/refresh",
            "token": "",
            "req_type": "POST",
            "access_role": "Authenticated"
        },
        {
            "name": "collections",
            "endpoint": f"{domain_name}/store/collections",
            "token": "JWT",
            "req_type": "GET, POST",
            "access_role": "Public, Admin"
        },
        {
            "name": "collection-detail",
            "endpoint": f"{domain_name}/store/collections/<int:pk>",
            "token": "JWT",
            "req_type": "PUT, DELETE",
            "access_role": "Admin"
        },
        {
            "name": "products",
            "endpoint": f"{domain_name}/store/products",
            "token": "JWT",
            "req_type": "GET, POST",
            "access_role": "Public, Admin"
        },
        {
            "name": "product-detail",
            "endpoint": f"{domain_name}/store/products/<int:pk>",
            "token": "JWT",
            "req_type": "PUT, DELETE",
            "access_role": "Admin"
        },
        {
            "name": "carts",
            "endpoint": f"{domain_name}/store/carts",
            "token": "JWT",
            "req_type": "GET, POST",
            "access_role": "Authenticate"
        },
        {
            "name": "cart-detail",
            "endpoint": f"{domain_name}/store/carts/<int:cart_pk>",
            "token": "JWT",
            "req_type": "PUT, DELETE",
            "access_role": "Authenticated"
        },
        {
            "name": "cart-items",
            "endpoint": f"{domain_name}/store/carts/<int:cart_pk>/items/",
            "token": "JWT",
            "req_type": "GET, POST",
            "access_role": "Authenticated"
        },
        {
            "name": "cart-items-add",
            "endpoint": f"{domain_name}/store/carts/<int:cart_pk>/items/<int:cart_items_pk>",
            "token": "JWT",
            "req_type": "GET, PATCH",
            "access_role": "Authenticated"
        },
        {
            "name": "orders",
            "endpoint": f"{domain_name}/store/orders",
            "token": "JWT",
            "req_type": "GET, POST",
            "access_role": "Authenticate"
        },
        {
            "name": "order-detail",
            "endpoint": f"{domain_name}/store/orders/<int:pk>",
            "token": "JWT",
            "req_type": "PUT, DELETE",
            "access_role": "Authenticated, Admin"
        },
    ]

    return all_domains