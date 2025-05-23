from django.db import models
from django.conf import settings
from products.models import Product
from users.models import User

# Create your models here.
class Cart(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.user.username}のカート"
  
  def get_total_price(self):
    return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
  cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=0)

  def __str__(self):
    return f"{self.product.name} x {self.quantity}"

class Order(models.Model):
  user = models.ForeignKey(User, verbose_name='購入者アドレス', on_delete=models.CASCADE)
  created_at = models.DateTimeField("購入日" ,auto_now_add=True)
  address = models.CharField("送付先住所" ,max_length=255)
  total_price = models.IntegerField("購入金額")

  def __str__(self):
    return f"{self.user.username}"
  
  class Meta:
    verbose_name = '購入履歴'
    verbose_name_plural = '購入一覧'
  
class OrderItem(models.Model):
  order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
  product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="商品",)
  quantity = models.PositiveIntegerField('数量')

  def __str__(self):
    return f"{self.product.name} x {self.quantity}"
  

  class Meta:
    verbose_name = "注文商品"
    verbose_name_plural = "注文商品の一覧"
