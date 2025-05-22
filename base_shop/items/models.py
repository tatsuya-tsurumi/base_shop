from django.db import models
from django.utils.text import slugify

# Create your models here.
class Item(models.Model):
  name = models.CharField("商品名", max_length=100)
  category = models.CharField("カテゴリ" ,max_length=50)
  manufacturer = models.CharField("メーカー" ,max_length=50)
  color = models.CharField("色(カラー)" ,max_length=30)
  position = models.CharField("ポジション(グローブのみ)" ,max_length=30)
  description = models.TextField("説明")
  image = models.ImageField("画像" ,upload_to='item_images')
  price = models.PositiveBigIntegerField("金額")
  slug = models.SlugField("スラッグ" ,unique=True, blank=True)

def save(self, *args, **kwargs):
  if not self.slug:
    self.slug = slugify(self.name) 
  super().save()

  def __str__(self):
    return self.name