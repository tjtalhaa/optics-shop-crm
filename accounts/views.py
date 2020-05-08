from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import OrderForms


def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    ready = orders.filter(status='Ready').count()
    delivered = orders.filter(status='Delivered').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'ready': ready}

    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


def customer(request, pk):

    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    total_orders = orders.count()
    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders
    }

    return render(request, 'accounts/customer.html', context)


def create_order(request):

    form = OrderForms()
    if request.method == 'POST':
        form = OrderForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }

    return render(request, 'accounts/order_form.html', context)


def update_order(request, pk):

    order = Order.objects.get(id=pk)
    form = OrderForms(instance=order)

    if request.method == 'POST':
        form = OrderForms(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'accounts/delete.html', context)
