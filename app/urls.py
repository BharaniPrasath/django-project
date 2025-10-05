from django.urls import path

from . import views_login
from . import views_seller
from . import views_addproduct
from . import views_cart



urlpatterns = [
    # --- Login
    path('signup/',views_login.signup),
    path('login/',views_login.login),
    path('logout/',views_login.logout),
    
    # --- Seller
    path('seller_signup/',views_seller.seller_signup),
    path('seller_login/',views_seller.seller_login),
    path('seller_logout/',views_seller.seller_logout),
    
    # Mobile Product
    path('addProduct/',views_addproduct.mobileProduct),
    path('getProduct/',views_addproduct.getProduct),
    path('getProductbyID/<int:id>/',views_addproduct.getProductByID),
    
    
    # Cart 
    path('getCartItem/',views_cart.getCartItem),
    path('addtocart/',views_cart.add_to_cart),
    path('deletecart/<int:item_id>/',views_cart.delete_cart_item),
    path('cart/update/<int:item_id>/', views_cart.update_cart_item, name='update-cart-item'),


]
