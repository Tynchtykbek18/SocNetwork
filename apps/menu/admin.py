from django.contrib import admin

from .models import Dish, Menu


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("id", "menu", "dish_name")
    list_display_links = ("id", "menu", "dish_name")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date")
    list_display_links = ("id", "title")
