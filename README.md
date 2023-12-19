
# To Do Web App

App practica, sencilla e intuitiva para registrar llevar un registro de las tareas del dia a dia la cual realiza un CRUD completo.


## Tecnologias Utilizadas

**Backend**

-Python

-Django

-SQL Lite

**FrontEnd**

-HTML

-Bootstrap


## Instalacion

Usando Conda creamos nuestro entorno virtual en la terminal del PC o desde el IDE que usemos y activamos el entorno.

```bash
  conda create --name nombre_del_entorno
  conda activate nombre_entorno
```

Instalamos el framework django y django-rest-framework

```bash
  pip install django
  pip install djangorestframework

```

## Creacion y Configuracion del Proyecto
En la terminal, creamos el proyecto, nos movemos a la carpeta del proyecto creado y seguido creamos la aplicion del proyecto.
```bash
  django-admin startproject nombre-proyecto
  cd nombre-proyecto
  python manage.py startapp proyecto-app

```

Agregamos en INSTALLED_APPS el nombre de nuestra aplicacion

```bash
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # añadimos
    'proyecto-app', #añadimos la app
]

```

## Creamos nuestros modelos
En el archivo ToDoApp/models.py
```bash
from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Task(models.Model):
    Titulo = models.CharField(max_length=50)
    Descripcion = models.TextField(blank=True)
    Fecha_creacion = models.DateField(auto_now_add=True)
    Completado = models.BooleanField(default=False )
    Fecha_completado = models.DateField(null=True, blank=True)
    Usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Titulo + '  -  Creado por: ' + self.Usuario.username
    
```

En la terminal realizamos las migraciones para la base de datos y para crear la tabla de la base de datos que viene integrada con Django, ejecutamos los comandos:

```bash
python manage.py makemigrations myapp
python manage.py migrate
```

## Vistas
Creamos cada una de las vistas que necesitaremos.

**Vista de inicio:** procesara las request que reciba, y devolvera la vista de la pagina HTML "home.html" (Mas adelante veremos los templates)
```bash
def home(request):
    return render(request, 'home.html')
```

**Vista de registro usuarios:**  Maneja el proceso de registro de usuarios. Si la solicitud es GET, se muestra la página de registro con un formulario vacío. Si la solicitud es de tipo POST (cuando se envía el formulario), verifica que las contraseñas coincidan.
Si coinciden, intenta crear un nuevo usuario con la información proporcionada.
Si tiene éxito, inicia sesión con el nuevo usuario y redirige a la página de tareas.
Si hay algún error (nombre de usuario duplicado), muestra un mensaje de error en la página de registro.

```bash
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

```

**Vista iniciar sesion:** Maneja las solicitudes GET Request: Muestra la página de inicio de sesión con un formulario vacío.
POST Request: Intenta autenticar al usuario con las credenciales proporcionadas. Si la autenticación es exitosa, inicia sesión y redirige a la página de tareas (tasks). Si la autenticación falla, muestra la página de inicio de sesión con un mensaje de error. Para el formulario, importamos de Django.

```bash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
```

**Vista cerrar sesion:** Realiza el cierre de sesión del usuario y redirige a la página de inicio (home). 


```bash
def cerrar_sesion(request): 
    logout(request)
    return redirect('home')
```

**Vista tareas:** Filtra las tareas asociadas al usuario actual que aún no han sido completadas. Luego, renderiza la página 'task.html' mostrando esas tareas.

```bash
def tasks(request):
    tasks = Task.objects.filter(Usuario=request.user, Fecha_completado__isnull=True) #se filtran las tareas por usuario y las que no estan completadas
    return render(request, 'task.html', {'tasks': tasks})
```

**Vista crear tareas:** Si la solicitud es de tipo GET, muestra la página 'crear_tareas.html' con un formulario vacío.
Si la solicitud es de tipo POST, intenta crear una nueva tarea con la información proporcionada.
Si la creación es exitosa, la asocia al usuario actual y redirige a la página de tareas (tasks).
Si hay un error (por ejemplo, campos incompletos), muestra la página 'crear_tareas.html' con un mensaje de error.

```bash
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

```


**Detalle de las Tareas:** Si la solicitud es de tipo GET, obtiene la tarea con el identificador task_id asociada al usuario actual y muestra la página 'tareas_detalles.html' con el formulario de la información de la tarea.
Si la solicitud es de tipo POST, actualiza la tarea con la información proporcionada.
Si la actualización es exitosa, redirige a la página de tareas (tasks).
Si hay un error (datos incorrectos), muestra la página 'tareas_detalles.html' con el mensaje de error.

```bash
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

```


**Vista Completar Tareas:** Marca las tareas como completadas. Obtiene la tarea con el identificador task_id asociada al usuario actual.
Si la solicitud es de tipo POST, actualiza la tarea estableciendo la fecha de completado y marcándola como completada.
Después de completar la tarea, redirige a la página de tareas (tasks).

```bash
def completar_tarea(request, task_id):
    task = get_object_or_404(Task, pk=task_id, Usuario=request.user)
    if request.method == 'POST':
        task.Fecha_completado = timezone.now()
        task.Completado = True
        task.save()
        return redirect('tasks')
```


**Tareas Completadas:** Muestra las tareas completadas y filtra las tareas del usuario actual que han sido completadas, ordena las tareas por la fecha en que fueron completadas de manera descendente. Renderiza la página 'tareas_completadas.html' con las tareas obtenidas.

```bash
def tasks_completed(request):
    tasks = Task.objects.filter(Usuario=request.user, Fecha_completado__isnull=False).order_by('-Fecha_completado') #se filtran las tareas por usuario y las que no estan completadas
    return render(request, 'tareas_completadas.html', {'tasks': tasks})
```


**Vista Eliminar tareas:** Elimina una tarea asociada al usuario actual. Obtiene la tarea con el identificador task_id asociada al usuario actual.
Si la solicitud es de tipo POST, elimina la tarea.
Después de eliminar la tarea, redirige a la página de tareas (tasks).


```bash
from django.shortcuts import render, redirect, get_object_or_404

def eliminar_tarea(request, task_id):
    task = get_object_or_404(Task, pk=task_id, Usuario=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
```


## IMPORTANTE: 
Cada una de las vistas que requieran que el usuario tenga sesion iniciada debe de llevar un decorador que solicite credenciales para iniciar sesion, de lo contrario cualquiera podria acceder a los endpoints a los cuales solo un usuario autenticado podria acceder.

Importamos y usamos el decorador:
```bash
from django.contrib.auth.decorators import login_required



@login_required             #Ejemplo
def tasks_completed(request):
```


**Creamos el archivo python de las URLS del proyecto**

```bash
from django.contrib import admin
from django.urls import path
from ToDoApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('logout', views.cerrar_sesion, name='logout'),
    path('signin/', views.iniciar_sesion, name='signin'),
    path('tasks/create/', views.crear_tarea, name='crear_tarea'),
    path('tasks/<int:task_id>', views.detalle_tarea, name='detalle_tarea'),
    path('tasks/<int:task_id>/complete', views.completar_tarea, name='completar_tarea'),
    path('tasks/<int:task_id>/delete', views.eliminar_tarea, name='eliminar_tarea'),
    path('tasks_completed/', views.tasks_completed , name='tasks_completed')

```


**Creamos un template main para que este le herede la estructura en todos los templates que creemos para las vistas**

Añadimos una etiqueta <link> donde enlazaremos a bootstrap para todo el diseño de los templates.
```bash

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>To Do List CRUD</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>

```


Siempre en el main de HTML, creamos elementos nav para poder navegar a cada template

```bash
<nav class="navbar navbar-expand-lg navbar navbar-dark bg-primary card card-body">
  {% if user.is_authenticated %}
    <div class="container">
    <a class="navbar-brand" href="#">Bienvenid@ {{ user.username }}</a>
        {% endif %}
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
            <a href = "/" class="nav-link">Inicio</a>
        </li>


        {% if user.is_authenticated %}
<!--        <li class="nav-item">-->
<!--            <a>Bienvenido {{ user.username }}</a>-->
<!--        </li>-->
        <li class="nav-item">
            <a href = "/tasks" class="nav-link">Tareas Pedientes</a>
        </li>
         <li class="nav-item">
            <a href = "/tasks_completed" class="nav-link">Tareas Completadas</a>
        </li>
        <li class="nav-item">
            <a href = "/tasks/create" class="nav-link">Crear Tarea</a>
        </li>
        <li class="nav-item">
            <a href = "/logout" class="nav-link">Cerrar Sesión</a>
        </li>
        {% else %}
        <li class="nav-item">
            <a href = "/signin" class="nav-link">Iniciar Sesión</a>
        </li>
        <li class="nav-item">
            <a href = "/signup" class="nav-link">Registrarse</a>
        </li>

        {% endif %}
      </ul>
    </div>
  </div>
</nav>





<nav>
    <ul>


    </ul>
</nav>



{% block content %}
{% endblock %}

</body>
</html>

```

**De aqui en adelante se crean los templates al gusto, importante al inicio de cada html escribir para que herede toda la estructura del main html.**


```bash
{% extends "base.html" %}
```

**Ahora solo ejecuta para probar en vivo la app**

```bash
python manage.py runserver
```

## Screenshots

<img width="1440" alt="Captura de pantalla 2023-12-19 a la(s) 12 27 25 a  m" src="https://github.com/ddpadilla/To-Do-App/assets/111556958/d475831a-d39d-4e56-b0c3-d630dc58f05a">


<img width="1440" alt="Captura de pantalla 2023-12-19 a la(s) 12 27 40 a  m" src="https://github.com/ddpadilla/To-Do-App/assets/111556958/cad4742d-1797-4fb5-94b6-b7a51846fc6b">


<img width="1440" alt="Captura de pantalla 2023-12-19 a la(s) 12 28 32 a  m" src="https://github.com/ddpadilla/To-Do-App/assets/111556958/df9bf0ed-e455-47ea-b6df-ba32e0c4047d">
