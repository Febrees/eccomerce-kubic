from store.utils import cartData
from django.shortcuts import render


def cart_data(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return context