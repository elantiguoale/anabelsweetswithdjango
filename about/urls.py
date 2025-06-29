from . import views
from django.urls import path


urlpatterns = [
    path('', views.about , name='home'),
    path('wall-of-fame/', views.wall_of_fame, name='wall_of_fame'),
    path('submit-cake/', views.submit_cake, name='submit_cake'),
    path('order/', views.order_cake, name='order_cake'),
    path('my-orders/', views.my_orders, name='my_orders'),
]