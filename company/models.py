from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, related_name='city', on_delete=models.CASCADE)
    title = models.ForeignKey(Title, related_name='title', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
