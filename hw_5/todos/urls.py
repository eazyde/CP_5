from django.urls import path
from .views import TodoListView, TodoDetailView, create_todo, TodoDeleteView, index, user_logout
from django.conf.urls.static import static
from hw_5 import settings

urlpatterns = [
    path('', index, name='index'),
    path('todos/', TodoListView.as_view(), name='todo_list'),
    path('todos/<int:pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('todos/create/', create_todo, name='create_todo'),
    path('todos/<int:pk>/delete/', TodoDeleteView.as_view(), name='todo_delete'),
    path('logout/', user_logout, name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)