"""
URL configuration for ToDoList project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
]
