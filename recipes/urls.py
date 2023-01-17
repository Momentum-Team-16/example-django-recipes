"""recipes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from core import views as core_views

urlpatterns = [
    path("", core_views.recipe_list, name="homepage"),
    path("recipes", core_views.recipe_list, name="recipe_list"),
    path("recipes/<int:pk>", core_views.recipe_detail, name="recipe_detail"),
    path("recipes/new", core_views.add_recipe, name="add_recipe"),
    path(
        "recipes/<int:recipe_pk>/ingredients",
        core_views.add_ingredient,
        name="add_ingredient",
    ),
    path("recipes/<int:recipe_pk>/copy", core_views.copy_recipe, name="copy_recipe"),
    path(
        "recipes/<int:recipe_pk>/add_recipe_step/",
        core_views.add_recipe_step,
        name="add_recipe_step",
    ),
    path("mealplan/", core_views.show_meal_plan, name="todays_meal_plan"),
    path(
        "mealplan/<int:year>/<int:month>/<int:day>/",
        core_views.show_meal_plan,
        name="show_meal_plan",
    ),
    path(
        "mealplan/add-remove/",
        core_views.meal_plan_add_remove_recipe,
        name="add_remove_recipe",
    ),
    path("admin/", admin.site.urls),
    path("accounts/", include("registration.backends.simple.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
