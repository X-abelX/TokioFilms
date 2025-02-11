from django.db import models

class categoryFilms(models.Model):
    name = models.CharField(max_length=100)
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['position']
    
class film(models.Model):
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
    age = models.CharField(max_length=2, choices=age_choices)
    releaseDate = models.DateField()
    duration = models.IntegerField()
    videoQuality = [
        ('HD', 'HD'),
        ('Full HD', 'Full HD'),
        ('Ultra HD', 'Ultra HD'),
        ('HDR', 'HDR'),
    ]
    videoQuality = models.CharField(max_length=10, choices=videoQuality)
    cast = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name