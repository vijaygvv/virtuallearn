from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('sign-up', views.sign_up, name='sign_up'),
    
    path('create-post', views.create_post, name='create_post'),
    path('editpost/<int:id>/', views.edit_post, name='edit_post'),
    path('updatepost/<int:id>/', views.update_post, name='update_post'),
    # path('deletepost/<int:id>/', views.delete_post, name='delete_post'),

    path('mypost', views.my_post, name='my_post'),
    path('mycart/', views.my_cart, name='my_cart'),
    path('myorder/', views.my_order, name='my_order'),

    path('charge/', views.charge, name='charge'),
    path('config/', views.stripe_config),

    path('create-checkout-session/', views.create_checkout_session), # new


]
