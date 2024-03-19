from django.urls import path
from OrderProcessingApp.views import *

urlpatterns = [
    path('', home, name="home"),
    path('settings/', orderSettings, name="ordersettings"),
   
    path('update/<int:pk>/', updateItem, name="updateOrderItem"),
    path('inventory/', inventoryManagement, name="inventorymanagement"),
    path('login', loginView , name='login'),
    path('login/validate/user/', login, name="validateUser" ),
    path('logout/', logout , name='logoutUserAccount'),
    path('register/', createaccount , name='createnewAccount'),
]