from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^BadArea/', include('BadArea.urls')),
    url(r'^admin/', admin.site.urls),
]

