from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path("", views.HomeView.as_view(), name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_request, name="logout"),
    path('ingredients/', views.IngredientsView.as_view(), name="ingredients"),
    path('ingredients/new', views.NewIngredientView.as_view(), name="add_ingredient"),
    path('ingredients/<pk>/update', views.UpdateIngredientView.as_view(), name="update_ingredient"),
    path('ingredients/<pk>/delete', views.DeleteIngredientView.as_view(), name="delete_ingredient"),
    path('purchases/', views.PurchasesView.as_view(), name="purchases"),
    path('purchases/new', views.NewPurchaseView.as_view(), name="new_purchase"),
    path('menu/', views.MenuItemsView.as_view(), name="menu"),
    path('menu/new', views.NewMenuItem.as_view(), name="add_menu_item"),
    path('reciperequirement/new', views.NewRecipeRequirementView.as_view(), name="add_recipe_requirement"),
    path('reports/', views.ReportView.as_view(), name="reports"),
    
]