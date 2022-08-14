from sre_constants import CATEGORY
from sre_parse import CATEGORIES
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
CATEGORIES = (
    ('VT', 'Vegetarian'),
    ('VE', 'Vegan'),
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner'),
)

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    servings = models.IntegerField()
    preptime = models.IntegerField()
    cookingtime = models.IntegerField()
    category = models.CharField(
        max_length=2,
        choices=CATEGORIES,
        default=CATEGORIES[0][0]
    )
    method = models.TextField(max_length=1000)
    # ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.title

