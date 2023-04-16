from django.db import models

# Create your models here.

class Equipo (models.Model):
    nombre = models.CharField(max_length=20)
    camada = models.IntegerField()
    
    def __str__(self):
        return f"{self.id} - {self.nombre} - {self.camada}"