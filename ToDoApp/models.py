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
    
