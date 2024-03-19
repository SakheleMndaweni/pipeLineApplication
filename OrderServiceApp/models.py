from django.db import models
from django.contrib.auth.models import User
import uuid
import random
"""
Pipeline OrderService Api Models
Task : 1

Author: Sakhele Mndaweni
Date: 2024/03/09/
"""
class OrderClient(models.Model):
        """
         Order class intance variables to keep track of the order Client object state 
        """
        user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
        name = models.CharField(max_length=200, null=True)
        email = models.CharField(max_length=200)
        # returns The Name of the OrderClient
        def __str__(self):
            return self.name

def random_id(length):
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0,length,2):
        id += random.choice(alpha)
    return id

def default_function():
    return  random_id(10)

class Product(models.Model):
            name = models.CharField(max_length=200)
            description = models.TextField(null=True)
            image = models.ImageField(upload_to='images/products',null=True, blank=True)
            itemCode =  models.CharField(
                            max_length = 14,
                            blank=True,
                            editable=False,
                            default= default_function
                            )

            def __str__(self):
                return self.name +' '+ self.description

            @property
            def imageURL(self):
                try:
                    url = self.image.url
                except:
                    url = ''
                return url

class Order(models.Model):
        """
          Order class intance variables to keep track of the order object state 
        """
        orderClient= models.ForeignKey(OrderClient, on_delete=models.SET_NULL, null=True, blank=True)
        orderDate = models.DateTimeField(auto_now_add=True)
        orderStatus = models.CharField(max_length=255, null=True)
        # returns the order id as a string
        def __str__(self):
            return str(self.id)

        # returns the current number of items in the order
        @property
        def getNumberOfitems(self):
            orderitems = self.orderitem_set.all()
            total = sum([item.quantity for item in orderitems])
            return total



class OrderItem(models.Model):
        """
        Order class 
        """
        product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
        order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
        quantity = models.IntegerField(default=0, null=True, blank=True)
        date = models.DateTimeField(auto_now_add=True)
       
       


