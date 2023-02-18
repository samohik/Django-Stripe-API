from . import views
from django.urls import path


app_name = 'payment'


urlpatterns = [
    path('', views.ItemsView.as_view(), name='items'),
    path('order/<int:pk>/', views.OrderView.as_view(), name='order'),
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('buy/<int:id>/', views.BuyView.as_view(), name='buy'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('cancel/', views.CancelView.as_view(), name='cancel'),
]
