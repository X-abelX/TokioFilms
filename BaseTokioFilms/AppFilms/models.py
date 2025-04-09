#Importamos los modelos de Django.
from django.db import models
from django.contrib.auth.models import User

#En este apartado creamos la tabla de categorias. Tanto peliculas como series.

class categoryFilms(models.Model):
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['position']


#En este apartado creamos la tabla de peliculas y series. Diferenciando entre si por el campo "type". Tienen relacion con la tabla de categorias.

class film(models.Model):
    CATEGORY_CHOICES = [
        ('pelicula', 'Película'),
        ('serie', 'Serie'),
    ]

    categoryFilms = models.ForeignKey(categoryFilms, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='portadas/')
    age_choices = [
        ('A', 'A'),
        ('7', '7'),
        ('12', '12'),
        ('15', '15'),
        ('18', '18'),
    ]
    likes = models.PositiveIntegerField(default=0)
    age = models.CharField(max_length=2, choices=age_choices)
    releaseDate = models.DateField()
    duration = models.IntegerField(null=True, blank=True)  # duration is optional for series
    videoQuality_choices = [
        ('HD', 'HD'),
        ('Full HD', 'Full HD'),
        ('Ultra HD', 'Ultra HD'),
        ('HDR', 'HDR'),
    ]
    videoQuality = models.CharField(max_length=10, choices=videoQuality_choices)
    cast = models.CharField(max_length=100)
    
    # Additional fields for series
    seasons = models.PositiveIntegerField(null=True, blank=True)
    episodes = models.PositiveIntegerField(null=True, blank=True)
    type = models.CharField(max_length=10, choices=CATEGORY_CHOICES, null=True)  # 'pelicula' or 'serie'

    def __str__(self):
        return self.title

#En este apartado creamos la tabla de likes. Tiene relacion con los datos del usuario y la tabla de peliculas. Su funcion es guardar los datos del usuario y la pelicula que le dio like.

class UserLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(film, on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')
    

#En este apartado creamos la tabla de listas. Tiene relacion con los datos del usuario y la tabla de peliculas. Su funcion es guardar los datos del usuario y la pelicula que le dio Añadir a mi lista.

class userlistadd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(film, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'film')