from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from users.models import Address

# カート表示
@login_required
def view_cart(request):
  cart, _ = Cart.objects.get_or_create(user=request.user)
  cart_items = cart.items.all()
  items_with_subtotals = []
  total_price = 0

  for item in cart_items:
        subtotal = item.product.price * item.quantity
        total_price += subtotal
        items_with_subtotals.append({
            'id': item.id,
            'product': item.product,
            'quantity': item.quantity,
            'subtotal': subtotal
        })
    
  referer = request.META.get('HTTP_REFERER', '/')

  return render(request, 'orders/cart_item.html', {
    'cart_items': items_with_subtotals,
    'total_price': total_price,
    'back_url': referer
    })

# カートに商品追加
@login_required
def add_to_cart(request, product_id):
  product = get_object_or_404(Product, id=product_id)
  cart, _ = Cart.objects.get_or_create(user=request.user)
  item, created = CartItem.objects.get_or_create(cart=cart, product=product)
  item.quantity += 1
  item.save()

  if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    return JsonResponse({'name': product.name, 'quantity': item.quantity})

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
  referer = request.META.get('HTTP_REFERER', '/')
  return redirect(referer)

# 購入処理。購入後カート内商品は削除
@login_required
def order_confirm_view(request):
  cart = Cart.objects.filter(user=request.user).first()
  cart_items = cart.items.all()
  total_price = sum(item.product.price * item.quantity for item in cart_items)
  referer = request.META.get('HTTP_REFERER', '/')
  items_with_subtotals = []

  for item in cart_items:
    subtotal = item.product.price * item.quantity
    items_with_subtotals.append({
      'id': item.id,
      'product': item.product,
      'quantity': item.quantity,
      'subtotal':subtotal
    })

  if 'temporary_address' in request.session:
    ship_address = request.session['temporary_address']
  else:
    address = get_object_or_404(Address, user=request.user)
    ship_address = {
      'postal_code': address.postal_code,
      'country': address.country,
      'prefecture': address.prefecture,
      'city': address.city,
      'street': address.street
    }
  if request.method == 'POST':
    prefecture = request.POST.get('prefecture', "")
    city = request.POST.get('city', "")
    street = request.POST.get('street', "")
    address_str = f"{prefecture}{city}{street}"
    order = Order.objects.create(
      user=request.user,
      address=address_str,
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
    'cart_items':items_with_subtotals,
    'total_price':total_price,
    'address':ship_address,
    'back_url': referer
  })
  

def order_complete_view(request):
  return render(request, 'orders/complete.html')

@login_required
def change_address_view(request):
  address, _ = Address.objects.get_or_create(user=request.user)
  referer = request.META.get('HTTP_REFERER', '/')
  if request.method == 'POST':
    postal_code = request.POST.get('postal_code', "")
    country = request.POST.get('country', "")
    prefecture = request.POST.get('prefecture', "")
    city = request.POST.get('city', "")
    street = request.POST.get('street', "")

    if postal_code and country and prefecture and city and street:
      request.session['temporary_address'] = {
        'postal_code': postal_code,
        'country': country,
        'prefecture': prefecture,
        'city': city,
        'street': street,
      }
      messages.success(request, 'お届け先住所を変更しました')
      return redirect('orders:confirm')
    else:
      messages.error(request, '全ての項目を入力してください')
  return render(request, 'orders/address.html', {
    'address':address,
    'back_url': referer,
  })

@login_required
def buy_now(request, product_id):
  product = get_object_or_404(Product, id=product_id)
  cart, _ = Cart.objects.get_or_create(user=request.user)
  item, created = CartItem.objects.get_or_create(cart=cart, product=product)
  item.quantity += 1
  item.save()

  return redirect('orders:confirm')