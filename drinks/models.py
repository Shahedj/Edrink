from django.db import models
#python manage.py makemigrations drinks


class Drink(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    cost = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/',  default='images/coffeeTwo.png' ) 

    #change the representation of an object
    def __str__(self):
        return self.name + ' ' + self.description