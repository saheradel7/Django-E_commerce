from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.get_products, name = 'get_products' ),
    path('products/new/',views.new_product, name = 'new_product' ),
    path('products/<str:pk>/',views.get_product, name = 'get_product' ),
    path('products/<str:pk>/update',views.update_product, name = 'update_product' ),
    path('products/<str:pk>/delete',views.delete_product, name = 'delete_product' ),
    path('<str:pk>/reviews',views.create_review, name = 'create_review' ),
    path('<str:pk>/reviews/delete',views.delete_review, name = 'delete_review' ),
    
]
