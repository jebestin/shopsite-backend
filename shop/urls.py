from django.urls import path
from . import views

urlpatterns = [
    path('shop-data/', views.get_shop_data, name='shop-data'),
    path('products/', views.get_products, name='products'),
    path('contact/', views.send_contact_message, name='contact'),
]
