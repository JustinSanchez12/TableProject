from django.urls import path
from . import views
urlpatterns = [
    path('interactive/', views.interactive_grid, name='interactive_grid'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('update/', views.update_grid, name='update_grid'),
]
