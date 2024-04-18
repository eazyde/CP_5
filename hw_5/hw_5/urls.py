from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from hw_5 import settings
from todos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todos.urls')),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)