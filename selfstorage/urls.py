from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', render, kwargs={'template_name': 'index.html'}, name='start_page'),
    path('', include('storage.urls')),
    path('faq/', render, kwargs={'template_name': 'faq.html'}, name='faq_page'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
