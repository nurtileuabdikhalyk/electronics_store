from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('shop/', views.shop, name='shop'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/order', views.order, name='order'),
    path('update_item/', views.updateItem, name='update_item'),
    path('category/<slug:slug>/', views.category, name='category'),
    path('accounts/login/', views.loginView, name='account_login'),
    path('accounts/signup/', views.signup, name='account_signup'),
    path("search/", views.Search.as_view(), name='search'),
    path('category/<slug:cat>/<slug:product_slug>/', views.single_product, name='single_product'),
]
