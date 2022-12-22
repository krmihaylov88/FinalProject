from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('FinalProject.cart.urls', namespace='cart')),
    path('account/', include('FinalProject.account.urls')),
    path('orders/', include('FinalProject.orders.urls', namespace='orders')),
    path('', include('FinalProject.shop.urls', namespace='shop')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
