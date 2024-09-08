from dataclasses import fields

from rest_framework import serializers
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

class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.__class__(value, context=self.context)
        return serializer.data

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    parent = RecursiveField('parent')

    class Meta:
        model = Category
        fields = '__all__'

class UnitSerializer(serializers.ModelSerializer):
    ancestors = RecursiveField('parent')

    class Meta:
        model = Unit
        fields = ['id', 'name', 'short_name', 'proportion_of_parent', 'ancestors']

class RecipySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipy
        fields = '__all__'

class IntakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intake
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    recipy = RecipySerializer('recipy')

    class Meta:
        model = Meal
        fields = '__all__'

class NutritionalElementSerializer(serializers.ModelSerializer):
    unit = UnitSerializer('unit')

    class Meta:
        model = NutritionalElement
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    brand = BrandSerializer('brand')
    category = CategorySerializer('category')

    class Meta:
        model = Ingredient
        fields = '__all__'

class PackageSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer('ingredient')
    unit = UnitSerializer('unit')

    class Meta:
        model = Package
        fields = '__all__'

class ConsumptionSerializer(serializers.ModelSerializer):
    package = PackageSerializer('package')
    meal = MealSerializer('meal')
    unit = UnitSerializer('unit')

    class Meta:
        model = Consumption
        fields = '__all__'

class RecipyCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer('category')
    recipy = RecipySerializer('recipy')
    unit = UnitSerializer('unit')

    class Meta:
        model = RecipyCategory
        fields = '__all__'

class NutritionSerializer(serializers.ModelSerializer):
    package = PackageSerializer('package')
    nutritional_element = NutritionalElementSerializer('nutritional_element')
    unit = UnitSerializer('unit')

    class Meta:
        model = Nutrition
        fields = '__all__'

class CategoryBrandSerializer(serializers.ModelSerializer):
    category = CategorySerializer('category')
    brand = BrandSerializer('brand')

    class Meta:
        model = CategoryBrand
        fields = '__all__'