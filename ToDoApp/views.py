from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': UserCreationForm()})
    else:
        #se crea un nuevo usuario
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except:
                return render (request, 'registro.html', {'form': UserCreationForm(), 'error': 'El usuario ya existe'})
        return render (request, 'registro.html', {'form': UserCreationForm(), 'error': 'Las contraseñas no coinciden'})

@login_required
def tasks(request):
    tasks = Task.objects.filter(Usuario=request.user, Fecha_completado__isnull=True) #se filtran las tareas por usuario y las que no estan completadas
    return render(request, 'task.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(Usuario=request.user, Fecha_completado__isnull=False).order_by('-Fecha_completado') #se filtran las tareas por usuario y las que no estan completadas
    return render(request, 'tareas_completadas.html', {'tasks': tasks})

@login_required
def crear_tarea(request):

    if request.method == 'GET':
        return render(request, 'crear_tareas.html', {
            'form': TaskForm()
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.Usuario = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'crear_tareas.html', {
                'form': TaskForm(),
                'error': 'Porfavor completa los campos'
            })


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

def iniciar_sesion(request):
    if request.method == 'GET':
        return render(request, "signin.html", {
            'form': AuthenticationForm()
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST
            ['password'])
        if user is None:
            return render(request, "signin.html", {
                'form': AuthenticationForm(),
                'error': 'Usuario y/o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('tasks')

@login_required
def detalle_tarea(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, Usuario=request.user)
        form = TaskForm(instance=task)
        return render(request, 'tareas_detalles.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, Usuario=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'tareas_detalles.html', {'task': task, 'form': form, 'error': 'Error actualizando la tarea'})

@login_required
def completar_tarea(request, task_id):
    task = get_object_or_404(Task, pk=task_id, Usuario=request.user)
    if request.method == 'POST':
        task.Fecha_completado = timezone.now()
        task.Completado = True
        task.save()
        return redirect('tasks')

@login_required
def eliminar_tarea(request, task_id):
    task = get_object_or_404(Task, pk=task_id, Usuario=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')