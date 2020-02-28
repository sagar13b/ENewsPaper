from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('surfer.urls')),
    path('account/',include('account.urls')),
    path('editor/',include('editor.urls')),
    path('admin/',include('publisher.urls')),
    path('api/',include('api.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)