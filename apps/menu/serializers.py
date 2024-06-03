from rest_framework import serializers

from .models import Dish, Menu


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"
        ref_name = "Dish"


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = "__all__"
        ref_name = "Menu"
