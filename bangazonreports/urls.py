from django.urls import path
from .views import completedorder_list

urlpatterns = [
    path('reports/orders/completed', completedorder_list),
]