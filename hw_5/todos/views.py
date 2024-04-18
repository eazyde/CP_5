from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Todo
from .serializers import TodoSerializer
from .forms import TodoForm
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .models import Todo
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from .forms import UserLoginForm, UserRegisterForm
from .serializers import TodoSerializer
from django.urls import reverse
from django.contrib.auth import logout


def index(request):
    todos = Todo.objects.all()
    return render(request, 'index.html', {'todos': todos})


class TodoListView(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TodoDetailView(generics.RetrieveAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Todo.objects.get(pk=self.kwargs.get('pk'))


class TodoDeleteView(DeleteView):
    model = Todo
    success_url = reverse_lazy('todo_list')


def create_todo(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('/todos/')
    else:
        form = TodoForm()
    return render(request, 'create_todo.html', {'form': form})


class TodoDeleteView(generics.DestroyAPIView):
    serializer_class = TodoSerializer

    def delete(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=kwargs['pk'])

        if todo.user != request.user:
            return Response({"error": "You don't have permission to delete this todo."},
                            status=status.HTTP_403_FORBIDDEN)

        todo.delete()

        return Response({"success": "Todo deleted successfully.", "redirect_to": reverse('index')},
                        status=status.HTTP_204_NO_CONTENT)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/todos/')
    else:
        form = UserLoginForm(request)
    return render(request, 'login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/todos/')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')