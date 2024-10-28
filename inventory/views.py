from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ingredient, MenuItem, RecipeRequirement, Purchase
from django.db.models import Sum, F
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context

class NewIngredientView(LoginRequiredMixin,CreateView):
    model = Ingredient
    template_name = "inventory/add_ingredient.html"
    form_class = IngredientForm

class UpdateIngredientView(LoginRequiredMixin,UpdateView):
    model = Ingredient
    template_name = "inventory/update_ingredient.html"
    form_class = IngredientForm

class IngredientsView(LoginRequiredMixin,ListView):
    model = Ingredient
    template_name = "inventory/view_ingredients.html"

class DeleteIngredientView(LoginRequiredMixin,DeleteView):
    model = Ingredient
    template_name = "inventory/delete_ingredient.html"
    success_url = "/ingredients"

class MenuItemsView(LoginRequiredMixin,ListView):
    model = MenuItem
    template_name = "inventory/view_menu_items.html"

class NewMenuItem(LoginRequiredMixin,CreateView):
    model = MenuItem
    template_name = "inventory/new_menu_item.html"
    form_class = MenuItemForm

class NewRecipeRequirementView(LoginRequiredMixin,CreateView):
    template_name = "inventory/add_recipe_requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm

class PurchasesView(LoginRequiredMixin,ListView):
    model = Purchase
    template_name = "inventory/view_purchases.html"

class NewPurchaseView(LoginRequiredMixin,TemplateView):
    model = Purchase
    template_name = "inventory/new_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all() if X.available()]
        return context
    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect("/purchases")


class ReportView(LoginRequiredMixin,TemplateView):
    template_name = "inventory/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.unit_price * \
                    recipe_requirement.quantity

        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = revenue - total_cost

        return context
    
def logout_request(request):
    logout(request)
    return redirect("home")
