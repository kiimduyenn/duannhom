from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DIVA.urls')),  # Tích hợp URL của ứng dụng diva
]
