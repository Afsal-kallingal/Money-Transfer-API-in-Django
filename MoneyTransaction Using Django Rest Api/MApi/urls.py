from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register_user),
    path('login/',views.user_login),
    path('create-wallet/<int:id>/',views.create_wallet),
    path('send-money/<int:id>/',views.send_money),
    path('add-money/<int:wallet_id>/',views.add_money),
    path('transactions/<int:id>/',views.transactions),
]
