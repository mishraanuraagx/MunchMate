from django.db import models

class Recipe(models.Model):
    RECIPE_TYPES = [
        (0, "Undefined"),
        (1, "Vegan"),
        (2, "Vegetarian"),
        (3, "Non-Vegetarian")
    ]

    name = models.CharField(max_length=255)
    recipe_type = models.IntegerField(default=0)
    details = models.TextField()

    def __str__(self):
        return self.name
