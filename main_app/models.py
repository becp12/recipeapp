from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date

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
    method = models.TextField()
    ingredients = models.TextField()

    def __str__(self):
        return f'{self.title} ({self.id})'

    def get_absolute_url(self):
        return reverse('home')

    class Meta:
        ordering = ['title']

class Comment(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created']


class TipTrick(models.Model):
    chef = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        ordering = ['-created']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for recipe_id: {self.recipe_id} @{self.url}"
