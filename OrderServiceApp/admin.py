from django.contrib import admin

# Register your models here.

from OrderServiceApp.models import *

admin.site.register(OrderClient)
admin.site.register(Order)
admin.site.register(OrderItem)

 