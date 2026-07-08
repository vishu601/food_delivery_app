from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    # Naye routes buttons ke liye
    path('cart/increase/<int:item_id>/', views.increase_cart, name='increase_cart'),
    path('cart/decrease/<int:item_id>/', views.decrease_cart, name='decrease_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
    path('signup/', views.signup_view, name='signup'),
   
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.otp_login_view, name='otp_login'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),

    path('login/', views.otp_login_view, name='login'), 
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    
   
]
