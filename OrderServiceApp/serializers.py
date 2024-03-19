from django.db.models import fields
from rest_framework import serializers
from .models import *

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = ('orderClient', 'orderDate', 'orderStatus')


class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ('name', 'description')
