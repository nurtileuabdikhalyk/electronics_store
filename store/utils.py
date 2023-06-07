from .models import *


def cartData(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)

    items = order.cart_set.all()

    cartItems = order.get_cart_items

    return {
        'items': items,
        'order': order,
        'cartItems': cartItems
    }
