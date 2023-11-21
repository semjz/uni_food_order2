from django.urls import path
from .views import (index, home, ChooseFood, OrderDetail, WalletDetail, OrdersDetail, ChargeWallet, AddFood
, ViewAllFoods, ViewFoodDetail)

app_name = 'order_food'

urlpatterns = [
    path("", index, name="index"),
    path("home/", home, name="home"),
    path("order-food/", ChooseFood.as_view(), name="order-food"),
    path("orders/<int:student_id>/", OrdersDetail.as_view(), name="orders-detail"),
    path("order/<int:order_id>/", OrderDetail.as_view(), name="order-detail"),
    path("wallet/<int:student_id>/", WalletDetail.as_view(), name="wallet-detail"),
    path("wallet/charge/<int:student_id>/", ChargeWallet.as_view(), name="charge-wallet"),
    path("food/create/", AddFood.as_view(), name="create-food"),
    path("foods/", ViewAllFoods.as_view(), name="foods-detail"),
    path("food/<int:food_id>/", ViewFoodDetail.as_view(), name="food-detail"),
]
