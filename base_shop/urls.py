
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from django.conf.urls.static import static # 画像用
from django.conf import settings # 画像用

urlpatterns = [
    path('admin/logout/', lambda request: redirect('/products/home/')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('', include('home.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 画像用
