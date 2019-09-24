from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


TYPES = (
    (0, "Fundacja"),
    (1, "Organizacja pozarządowa"),
    (2,"Zbiórka lokalna"),
)
class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.SmallIntegerField(choices=TYPES, default=0)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.SmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    adress = models.CharField(max_length=256)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=256)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField()
    pick_up_time = models.DateTimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
