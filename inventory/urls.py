from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('ingredients/', views.IngredientsView.as_view(), name='ingredients'),
    path('purchases/', views.PurchasesView.as_view(), name='purchases'),
    path('menu/', views.MenuItemsView.as_view(), name='menu'),
    path('reports/', views.ReportView.as_view(), name='reports'),
]