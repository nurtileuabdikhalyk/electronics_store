import datetime
import json

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .forms import AddressForm, LoginForm, CustomerForm
from .models import *
from .utils import cartData


def index(request):
    categories = Category.objects.all()
    products = Product.objects.order_by('-created')[:6]

    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
    else:
        cartItems = 0
        order = 0
    context = {
        'title': 'ALI',
        'products': products,
        'categories': categories,
        'cartItems': cartItems,
        'order': order,
    }
    return render(request, 'store/index.html', context)


# admin
# ali
def single_product(request, cat, product_slug):
    categories = Category.objects.all()
    product = get_object_or_404(Product, slug=product_slug)
    products = Product.objects.filter(category=product.category)[:6]
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
    else:
        cartItems = 0
        order = 0
    context = {
        'title': product.name,
        'product': product,
        'products': products,
        'categories': categories,
        'cartItems': cartItems,
        'order': order,
    }
    return render(request, 'store/single_product.html', context)


def shop(request):
    categories = Category.objects.all()
    products = Product.objects.order_by('-created')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    pages = paginator.get_page(page_number)
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
    else:
        cartItems = 0
        order = 0
    context = {
        'title': "Дүкен",
        'products': products,
        'pages': pages,
        'categories': categories,
        'cartItems': cartItems,
        'order': order,

    }
    return render(request, 'store/shop.html', context)


def category(request, slug):
    categories = Category.objects.all()
    cat = get_object_or_404(Category, slug=slug)
    if request.user.is_authenticated:
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
    else:
        cartItems = 0
        order = 0
    object_list = Product.objects.filter(category=cat)
    context = {
        "title": cat.name,
        "object_list": object_list,
        "categories": categories,
        "cartItems": cartItems,
        "order": order,
    }
    return render(request, 'store/search.html', context)


class Search(ListView):
    template_name = 'store/search.html'

    def get_queryset(self):
        return Product.objects.filter(name__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = 'Іздеу'
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context


def cart(request):
    data = cartData(request)

    products = Product.objects.order_by('created')[:2]
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    categories = Category.objects.all()
    context = {
        "title": "Себет",
        "categories": categories,
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "products": products,
    }
    return render(request, 'store/cart.html', context)


def order(request):
    categories = Category.objects.all()
    data = cartData(request)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)
    transaction_id = datetime.datetime.now().timestamp()
    items = data['items']
    for item in items:
        OrderItem.objects.create(order=order, transaction_id=transaction_id, product=item.product,
                                 quantity=item.quantity)
    context = {
        "title": "Тапсырыс",
        "categories": categories,
        "transaction_id": transaction_id,
    }
    items.delete()
    return render(request, 'store/order.html', context)


def checkout(request):
    data = cartData(request)
    if request.method == 'POST':
        form = AddressForm(request.user.customer, request.POST)
        print(form)
        if form.is_valid():
            form = form.save(commit=False)

            form.save()
            return redirect('order')
    form = AddressForm(request.user.customer)
    order = data['order']
    cartItems = data['cartItems']
    categories = Category.objects.all()
    context = {
        "title": "Чек",
        "categories": categories,
        "form": form,
        "order": order,
        "cartItems": cartItems,
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer)
    cart, created = Cart.objects.get_or_create(order=order, product=product)

    if action == 'add':
        cart.quantity = (cart.quantity + 1)
    if action == 'remove':
        cart.quantity = (cart.quantity - 1)
    cart.save()
    if cart.quantity <= 0:
        cart.delete()
    return JsonResponse('Added', safe=False)


def loginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['login']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            login(request, user)

            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            Customer.objects.create(user=user,
                                    first_name=form.cleaned_data['first_name'],
                                    last_name=form.cleaned_data['last_name'],
                                    email=form.cleaned_data['email'],
                                    phone=form.cleaned_data['phone'],

                                    )
            return redirect('home')
        else:
            error = 'Қолданушы табылмады'
    else:
        form = CustomerForm()

    context = {'form': form}
    return render(request, 'account/signup.html', context)
