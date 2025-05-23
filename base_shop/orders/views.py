from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required

# カート表示
@login_required
def view_cart(request):
  cart, created = Cart.objects.get_or_create(user=request.user)
  return render(request, 'orders/cart_item.html', {'cart':cart})

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
  if item.quantity > 1:
    item.quantity -= 1
    item.save()
  else:
    item.delete()
  return redirect('orders:view_cart')

# 購入処理。購入後カート内商品は削除
@login_required
def order_confirm_view(request):
  cart = Cart.objects.filter(user=request.user).first()
  ship_address = request.session.get('temporary_address', request.user.address)

  if request.method == 'POST':
    if not cart:
      return redirect('products:home')
    order = Order.objects.create(
      user=request.user,
      address=ship_address,
      total_price=cart.get_total_price()
    )

    for item in cart.items.all():
      OrderItem.objects.create(
        order=order,
        product=item.product,
        quantity=item.quantity
      )
    cart.items.all().delete()
    if 'temporary_address' in request.session:
      del request.session['temporary_address']
    return redirect('orders:order_complete')
  
  return render(request, 'orders/order.html', {
    'cart':cart,
    'cart_items':cart.items.all(),
    'address':ship_address,
  })
  

def order_complete_view(request):
  return render(request, 'orders/complete.html')

@login_required
def change_address_view(request):
  ship_address = request.user.address
  if request.method == 'POST':
    new_address = request.POST.get('ship_address')
    if new_address:
      request.session['temporary_address'] = new_address
      return redirect('orders:confirm')
  return render(request, 'orders/address.html', {
    'address':ship_address
  })