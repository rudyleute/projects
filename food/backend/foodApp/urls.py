from django.urls import path, include

from .views.brand_view import BrandView
from .views.meal_view import MealView
from .views.unit_view import UnitView
from .views.intake_view import IntakeView
from .views.recipy_view import RecipyView
from .views.nutrition_view import NutritionView
from .views.nutritional_element_view import NutritionalElementView
from .views.package_view import PackageView
from .views.recipy_category_view import RecipyCategoryView
from .views.category_brand_view import CategoryBrandView
from .views.category_view import CategoryView
from .views.consumption_view import ConsumptionView
from .views.ingredient_view import IngredientView
from .views.activity_level_view import ActivityLevelView

urlpatterns = [
    path('brand/', BrandView.as_view()),
    path('brand/<uuid:pk>/', BrandView.as_view()),
    path('category/', CategoryView.as_view()),
    path('category/<uuid:pk>/', CategoryView.as_view()),
    path('meal/', MealView.as_view()),
    path('meal/<uuid:pk>/', MealView.as_view()),
    path('unit/', UnitView.as_view()),
    path('unit/<uuid:pk>/', UnitView.as_view()),
    path('recipy/', RecipyView.as_view()),
    path('recipy/<uuid:pk>/', RecipyView.as_view()),
    path('intake/', IntakeView.as_view()),
    path('intake/<uuid:pk>/', IntakeView.as_view()),
    path('nutrition/', NutritionView.as_view()),
    path('nutrition/<uuid:pk>/', NutritionView.as_view()),
    path('nutrition_element/', NutritionalElementView.as_view()),
    path('nutrition_element/<uuid:pk>/', NutritionalElementView.as_view()),
    path('package/', PackageView.as_view()),
    path('package/<uuid:pk>/', PackageView.as_view()),
    path('recipy_category/', RecipyCategoryView.as_view()),
    path('recipy_category/<uuid:pk>/', RecipyCategoryView.as_view()),
    path('consumption/', ConsumptionView.as_view()),
    path('consumption/<uuid:pk>/', ConsumptionView.as_view()),
    path('ingredient/', IngredientView.as_view()),
    path('ingredient/<uuid:pk>/', IngredientView.as_view()),
    path('category_brand/', CategoryBrandView.as_view()),
    path('category_brand/<uuid:pk>/', CategoryBrandView.as_view()),
    path('activity_level/', ActivityLevelView.as_view()),
    path('activity_level/<uuid:pk>/', ActivityLevelView.as_view()),
]
