from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm, ProductForm, OrderFormUpdate
from .filters import OrderFilterGeneral, OrderFilterCustomer
from .decorators import unauthenticated_user, allowed_users, admin_only


# home
@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all().order_by('-id')
    customers = Customer.objects.all().order_by('-id')

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    ready = orders.filter(status='Ready').count()
    InWorkshop = orders.filter(status='In Workshop').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'ready': ready, 'InWorkshop': InWorkshop}

    return render(request, 'accounts/dashboard.html', context)

  # user-register-auth


@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('login')

    context = {'form': form}
    return render(request, 'userauth/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'userauth/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# user(customer) dashboard and settingspage
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all().order_by('-id')

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    ready = orders.filter(status='Ready').count()
    InWorkshop = orders.filter(status='In Workshop').count()

    print('ORDERS:', orders)

    context = {'orders': orders,
               'total_orders': total_orders, 'delivered': delivered,
               'ready': ready, 'InWorkshop': InWorkshop}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)

 # customer pannel but (admin access)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilterC = OrderFilterCustomer(request.GET, queryset=orders)
    orders = myFilterC.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilterC': myFilterC}
    return render(request, 'customer/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=('product', 'status', 'note'), extra=7)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'customer/create_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderFormUpdate(instance=order)
    print('ORDER:', order)
    if request.method == 'POST':

        form = OrderFormUpdate(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'customer/update_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'customer/delete_order.html', context)

 # orders pages with admin access


@login_required(login_url='login')
@admin_only
def ordersPannel(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    myFilter = OrderFilterGeneral(request.GET, queryset=orders)
    orders = myFilter.qs

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    ready = orders.filter(status='Ready').count()
    InWorkshop = orders.filter(status='In Workshop').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'delivered': delivered,
               'ready': ready, 'InWorkshop': InWorkshop, 'myFilter': myFilter}

    return render(request, 'accounts/orders_dashboard.html', context)


# product
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all().order_by('-id')

    return render(request, 'product/products.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def productsC(request):
    products = Product.objects.all().order_by('-id')

    return render(request, 'product/productsC.html', {'products': products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def addProduct(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {
        'form': form
    }
    return render(request, 'product/add_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance=product)
    if request.method == 'POST':

        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products')

    context = {'form': form}
    return render(request, 'product/update_product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == "POST":
        product.delete()
        return redirect('products')

    context = {'item': order}
    return render(request, 'product/delete_product.html', context)
