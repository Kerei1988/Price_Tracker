from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/add', views.add_product, name='add_product'),
    path('products/product/<int:id_product>/', views.product_detail, name='product_detail'),
    path('products/history/<int:id_product>/', views.history, name='history')
]