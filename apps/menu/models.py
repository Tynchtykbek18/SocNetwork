from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=255)
    date = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Dish(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="dishes")
    img_src = models.URLField(max_length=500)
    dish_name = models.CharField(max_length=255)
    dish_url = models.URLField(max_length=500)
    calorie = models.IntegerField()

    def __str__(self):
        return self.menu.title
