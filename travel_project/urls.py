from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('travel_agent.urls')),
]

# Раздаем только МЕДИА (картинки туров).
# Статику (CSS/JS) теперь раздает WhiteNoise автоматически.
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

handler404 = "travel_agent.views.exception_404"
handler403 = "travel_agent.views.exception_403"
handler500 = "travel_agent.views.exception_500"