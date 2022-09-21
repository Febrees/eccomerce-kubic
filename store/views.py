from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .utils import cartData
from .models import *
from .filters import ProductFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
    product_list = Product.objects.all().order_by("-viewed")
    categories = Category.objects.all()
    product_filter = ProductFilter(request.GET, queryset=product_list)
    paginator = Paginator(product_filter.qs, 12)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'store/products.html', {'myFilter': product_filter, 'products': products, 'categories': categories})


def product_detail(request, pk):
    product = Product.objects.get(id=pk)
    product.viewed += 1
    product.save()
    same_products = Product.objects.filter(category=product.category).exclude(id=pk)[:12]
    context = {'product':product, 'same_products':same_products}
    return render(request, 'store/product_detail.html', context)


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    categories = Category.objects.filter(parent=None)
    category_products = Product.objects.filter(category=category)
    
    context = {'products': category_products, 'categories': categories}
    return render(request, 'store/category.html', context)


def store(request):
    products = Product.objects.all()[:6]
    new_products = Product.objects.all().order_by("-updated_at")[:6]
    context = {'products': products, 'new_products': new_products}
    return render(request, 'store/index.html', context)


def cart(request):

    data = cartData(request)
    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order,}
    return render(request, 'store/basket.html', context)


# def checkout(request):

#     data = cartData(request)
#     items = data['items']
#     order = data['order']
#     cartItems = data['cartItems']
#     categories = Category.objects.filter(parent=None)

#     context = {'items': items, 'order': order, 'cartItems': cartItems, 'categories': categories}
#     return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


# def processOrder(request):
#     transaction_id = datetime.datetime.now().timestamp()
#     data = json.loads(request.body)

#     if request.user.is_authenticated:
#         customer, created = Customer.objects.get_or_create(
#             user=request.user, 
#             name=data['user-form']['name'],
#             phone=data['user-form']['phone']
#         )
#         order, created = Order.objects.get_or_create(
#             customer=customer, complete=False)
#     else:
#         customer, order = guestOrder(request, data)

#     total = float(data['user-form']['total'])
#     order.transaction_id = transaction_id

#     if total == order.get_cart_total:
#         order.complete = True
#     order.save()

#     if order.shipping == True:
#         ShippingAddress.objects.create(
#             customer=customer,
#             order=order,
#             country=data['shipping']['country'],
#             city=data['shipping']['city'],
#             address=data['shipping']['address'],
#             ex_address=data['shipping']['ex_address'],
#             zipcode=data['shipping']['zipcode']
#         )

#     return JsonResponse('Payment complete!', safe=False)