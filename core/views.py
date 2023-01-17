import datetime
import copy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from .models import Recipe
from .forms import RecipeForm, IngredientForm, RecipeStepForm


def recipe_list(request):
    recipes = (
        Recipe.objects.for_user(request.user)
        .annotate(
            times_favorited=Count("favorited_by", distinct=True),
            total_time_in_minutes=F("prep_time_in_minutes") + F("cook_time_in_minutes"),
        )
        .order_by("title")
    )
    if not request.user.is_authenticated:
        return redirect("auth_login")

    template_name = "core/recipe_list.html"

    return render(request, template_name, {"recipes": recipes})


def recipe_detail(request, pk):
    recipes = Recipe.objects.for_user(request.user).annotate(
        num_ingredients=Count("ingredients", distinct=True)
    )
    recipe = get_object_or_404(recipes, pk=pk)
    return render(
        request,
        "core/recipe_detail.html",
        {"recipe": recipe, "ingredient_form": IngredientForm()},
    )


@login_required
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(data=request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, "Recipe added!")
            return redirect("recipe_detail", pk=recipe.pk)

    else:
        form = RecipeForm()

    return render(request, "core/add_recipe.html", {"form": form})


@login_required
def add_ingredient(request, recipe_pk):
    recipe = get_object_or_404(request.user.recipes, pk=recipe_pk)

    if request.method == "POST":
        form = IngredientForm(data=request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)
            ingredient.recipe = recipe
            ingredient.save()

    return redirect("recipe_detail", pk=recipe.pk)


def add_recipe_step(request, recipe_pk):
    recipe = get_object_or_404(request.user.recipes, pk=recipe_pk)

    if request.method == "POST":
        form = RecipeStepForm(data=request.POST)

        if form.is_valid():
            recipe_step = form.save(commit=False)
            recipe_step.recipe = recipe
            recipe_step.save()

            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeStepForm()

    return render(
        request, "core/add_recipe_step.html", {"form": form, "recipe": recipe}
    )


@login_required
def copy_recipe(request, recipe_pk):
    original_recipe = get_object_or_404(Recipe, pk=recipe_pk)
    new_recipe = copy.deepcopy(original_recipe)
    new_recipe.pk = None
    new_recipe.original_recipe = original_recipe
    new_recipe.public = False
    new_recipe.save()

    for ingredient in original_recipe.ingredients.all():
        new_recipe.ingredients.create(amount=ingredient.amount, item=ingredient.item)

    return redirect("recipe_detail", pk=new_recipe.pk)


@login_required
def show_meal_plan(request, year=None, month=None, day=None):
    """
    Given a year, month, and day, look up the meal plan for the current user for that
    day and display it.

    If a form is submitted to add a recipe, then go ahead and add recipe to the
    meal plan for that day.
    """
    if year is None:
        date_for_plan = datetime.date.today()
    else:
        date_for_plan = datetime.date(year, month, day)
    next_day = date_for_plan + datetime.timedelta(days=1)
    prev_day = date_for_plan + datetime.timedelta(days=-1)

    # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#get-or-create
    meal_plan, _ = request.user.meal_plans.get_or_create(date=date_for_plan)
    recipes_not_in_mealplan = Recipe.objects.for_user(request.user).exclude(
        pk__in=[r.pk for r in meal_plan.recipes.all()]
    )

    return render(
        request,
        "core/show_mealplan.html",
        {
            "plan": meal_plan,
            "recipes_to_add": recipes_not_in_mealplan,
            "date": date_for_plan,
            "next_day": next_day,
            "prev_day": prev_day,
        },
    )


@login_required
@csrf_exempt
def meal_plan_add_remove_recipe(request):
    request_is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest"
    date = request.POST.get("date")
    recipe_pk = request.POST.get("pk")
    meal_plan, _ = request.user.meal_plans.get_or_create(date=date)
    recipe = Recipe.objects.for_user(request.user).get(pk=recipe_pk)

    meal_plan.add_or_remove_recipe(recipe)

    if request_is_ajax:
        return JsonResponse({}, status=204)

    return HttpResponse(status=204)
