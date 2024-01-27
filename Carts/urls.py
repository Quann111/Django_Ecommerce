from django.urls import path
from .views import*
urlpatterns = [
    path('Carts',CartView.as_view()),

]
