from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required

# カート表示
@login_required
def view_cart(request):
  cart, created = Cart.objects.get_or_create(user=request.user)
  return render(request, 'order/cart.html', {'cart':cart})

# カートに商品追加
@login_required
def add_to_cart(request, product_id):
  product = get_object_or_404(Product, id=product_id)
  cart, created = Cart.objects.get_or_create(user=request.user)
  item, created = CartItem.objects.get_or_create(cart=cart, product=product)
  item.quantity += 1
  item.save()
  return redirect('orders:view_cart')

# カートから商品削除
@login_required
def remove_from_cart(request, item_id):
  item = get_object_or_404(CartItem, id=item_id)
  item.delete()
  return redirect('orders: view_cart')

# 購入処理。購入後カート内商品は削除
@login_required
def checkout(request):
  cart = Cart.objects.get(user=request.user)
  if not cart.items.exists():
    return redirect('orders: view_cart')
  
  order = Order.objects.create(user=request.user)

  for item in cart.items.all():
    OrderItem.objects.create(
      order = order,
      product = item.product,
      quantity = item.quantity
    )

    cart.products.all().delete()

    return render(request, 'orders/checkout_success.html', {'order':order})