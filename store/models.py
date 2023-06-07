from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField('Есімі', max_length=200, )
    last_name = models.CharField('Тегі', max_length=200, )
    phone = models.CharField('Телефон', max_length=16)
    email = models.CharField('Почта', max_length=200, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Тұтынушы"
        verbose_name_plural = "Тұтынушылар"


class Category(models.Model):
    name = models.CharField('Категория аты', max_length=150)
    slug = models.SlugField('Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категориялар'

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField("Тауар аты", max_length=150)
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    price = models.DecimalField("Бағасы", max_digits=12, decimal_places=2)
    image = models.ImageField('Сурет', upload_to='products/')
    slug = models.SlugField('Слаг')
    description = models.TextField("Сипаттама")
    created = models.DateTimeField('Құрылған уақыты', auto_now_add=True)

    class Meta:
        verbose_name = 'Тауар'
        verbose_name_plural = 'Тауарлар'

    def __str__(self):
        return f"{self.name} {self.price} {self.created}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, verbose_name='Тұтынушы', on_delete=models.CASCADE)
    complete = models.BooleanField('Орындалды/Орындалмады', default=False)

    @property
    def get_cart_total(self):
        cart = self.cart_set.all()
        total = sum([item.get_total for item in cart])
        return total

    @property
    def get_cart_items(self):
        cart = self.cart_set.all()
        total = sum([item.quantity for item in cart])
        return total

    class Meta:
        verbose_name = 'Тапсырыс'
        verbose_name_plural = 'Тапсырыстар'

    def __str__(self):
        return f"{self.id} {self.customer}"


class Cart(models.Model):
    product = models.ForeignKey(Product, verbose_name='Тауар', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='Тапсырыс', on_delete=models.CASCADE)
    quantity = models.IntegerField('Саны', default=0, null=True, blank=True)
    created = models.DateTimeField('Құрылған уақыты', auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    class Meta:
        verbose_name = 'Себет'
        verbose_name_plural = 'Себет'

    def __str__(self):
        return f"{self.order.customer.first_name} {self.order.customer.last_name} {self.created}"


class Address(models.Model):
    CITY = [
        ('ALA', 'Алматы'),
        ('NQZ', 'Астана'),
        ('CIT', 'Шымкент'),
    ]
    customer = models.ForeignKey(Customer, verbose_name='Тұтынушы', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='Тапсырыс', on_delete=models.CASCADE)
    phone = models.CharField('Телефон №', max_length=20)
    street = models.CharField('Көше', max_length=30)
    home_number = models.IntegerField('Үй №')
    floor = models.IntegerField('Этаж №', null=True, blank=True)
    door = models.IntegerField('Пәтер №', null=True, blank=True)

    class Meta:
        verbose_name = 'Мекен-жай'
        verbose_name_plural = 'Мекен-жай'

    def __str__(self):
        return f"{self.customer.first_name} {self.phone}"


class ProductShots(models.Model):
    image = models.ImageField("Изображение", upload_to="product_shots/")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name = "Сурет"
        verbose_name_plural = "Суреттер"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, verbose_name='Тауар', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name='Тапсырыс', on_delete=models.CASCADE)
    quantity = models.IntegerField('Саны', default=0, null=True, blank=True)
    created = models.DateTimeField('Құрылған уақыты', auto_now_add=True)
    transaction_id = models.CharField("Тапсырыс номері", max_length=100, null=True)

    class Meta:
        verbose_name = 'Тапсырыс орны'
        verbose_name_plural = 'Тапсырыс орны'

    def __str__(self):
        return f"{self.order.customer.first_name} {self.order.customer.last_name} {self.created}"
