from django.urls import path, include
from . import views

urlpatterns =[
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Registrace a přihlášení
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Vinyly 
    path('vinyls/', views.vinyl_list, name='vinyl_list'),
    path('vinyls/<int:vinyl_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('add-vinyl/', views.add_vinyl, name='add_vinyl'),

    # Košík a objednávky 
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/', views.cart_view, name='cart'), 
    path('cart/<int:vinyl_id>/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),

    # Přidání hodnocení
    path('vinyls/<int:vinyl_id>/add-rating/', views.add_rating, name='add_rating'),

    #Privacy policy
    path('privacy/', views.privacy, name='privacy'),

    #Edit tlačítko
    path('vinyls/<int:vinyl_id>/edit/', views.edit_vinyl, name='edit_vinyl'),

    #Nahled vinylu 
    path('vinyl/<int:pk>/', views.vinyl_detail, name='vinyl_detail'),

 ]