from django.contrib import admin
from django.urls import include, path  # Import 'include' to connect other apps

urlpatterns = [
    path('admin/', admin.site.urls),  # Django admin panel
    path('sacco/', include('sacco_app.urls')),  # Connect sacco_app URLs
]
