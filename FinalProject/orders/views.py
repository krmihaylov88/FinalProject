from django.shortcuts import render

from FinalProject.cart.cart import Cart
from FinalProject.orders.forms import OrderCreateForm
from FinalProject.orders.models import OrderItem


# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            context = {
                'order': order
            }

            return render(request, 'orders/order/created.html', context)
    else:
        form = OrderCreateForm()
    context = {
        'cart': cart,
        'form': form
    }
    return render(request, 'orders/order/create.html', context)
