from rest_framework import viewsets
from django.shortcuts import render
from .models.brand import Brand
from .models.category import Category
from .models.category_brand import CategoryBrand
from .models.consumption import Consumption
from .models.ingredient import Ingredient
from .models.intake import Intake
from .models.meal import Meal
from .models.nutrition import Nutrition
from .models.nutritional_element import NutritionalElement
from .models.package import Package
from .models.recipy import Recipy
from .models.recipy_category import RecipyCategory
from .models.unit import Unit
from .serializers import *

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
# Create your views here.
