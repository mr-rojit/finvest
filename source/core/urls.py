from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company-details/', include('analytics.urls')),
    path('', include('companies.urls'))
]
