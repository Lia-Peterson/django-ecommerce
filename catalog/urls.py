from django.urls import path

# from . import views
from catalog import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.index, name='index'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('<int:product_id>/collection', views.collection, name='collection'),
    path('<int:product_id>/buy/', views.buy, name='buy')
    #path('<int:product_id>/1', views.detail) 
    ]
#views.detail = business logic 
#