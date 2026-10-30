from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travel_agent.urls')),
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': os.path.join(settings.BASE_DIR, 'static')}),
]


handler404 = "travel_agent.views.exception_404"
handler403 = "travel_agent.views.exception_403"
handler500 = "travel_agent.views.exception_500"