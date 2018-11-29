from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^example1/', include('example1.urls')),
    url(r'^.*/', include('businesses.urls')),
    url(r'^admin/', admin.site.urls),
]