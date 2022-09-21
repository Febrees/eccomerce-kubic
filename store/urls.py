from django.urls import path

from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('products/', views.product_list, name="product_list"),
	path('cart/', views.cart, name="cart"),
	path('product/<int:pk>/', views.product_detail, name="product_detail"),
	path('category/<slug:slug>/', views.category_detail, name="category"),

	path('update_item/', views.updateItem, name="update_item"),
]