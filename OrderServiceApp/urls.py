from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from OrderServiceApp.views import *

urlpatterns = [
    path('order/item/', ItemListApiView().as_view()),
    path('order/item/<int:pk>/', ItemApiView.as_view()),
    path('order/', updateItem),
    path('process/Order/<int:orderId>/', precessOrder)
]

urlpatterns = format_suffix_patterns(urlpatterns)