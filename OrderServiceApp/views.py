from OrderServiceApp.models import *
from OrderServiceApp.serializers import *
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from django.shortcuts import render
import json
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
import time
import aiohttp
import asyncio
from asgiref.sync import sync_to_async

class ItemListApiView(APIView):
    
            parser_classes = (MultiPartParser,FormParser,JSONParser)
            permission_classes = (AllowAny,)
            """
            Inventory List and post
            """
            def post(self, request, format=None):
                    serializer = ItemSerializer(data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            def get(self, request, format=None):
                    items = Product.objects.all()
                    serializer = ItemSerializer(item, many=True)
                    return Response(serializer.data)


class ItemApiView(APIView):
    """
    Retrieve, update or delete a product or item  instance.
    """
    parser_classes = (MultiPartParser,FormParser,JSONParser)
    permission_classes = (AllowAny,)
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse('Item saved',safe=False)
        return JsonResponse('Invalid Item data',safe=False)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Update items in the order
def updateItem(request):
    data = json.loads(request.body)
    priductId = data['itemId']
    action = data['action']
    customer = request.user.orderclient
    product_temp = Product.objects.get(id = priductId)
    order, created = Order.objects.get_or_create(orderClient=customer, orderStatus ='NotProcessed')
    orderItem, created = OrderItem.objects.get_or_create(order=order, product = product_temp)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    
    if orderItem.quantity <= 0 or action == 'removeAll':
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)
        

@sync_to_async
def get_all_order(order):
    return Order.objects.get(id = order)

@sync_to_async
def getProductCode(orderItem):
     return orderItem.product.itemCode

async def get_validation(session, url):
    async with session.get(url) as res:
        item_data = await res.json()
        return item_data


async def precessOrder(request,orderId):
    starting_time = time.time()
    order = await get_all_order(orderId) 
    items = []
            # getting all items related to the order that must be processed
    async for od in OrderItem.objects.filter(order = order):
            itemCode = await getProductCode(od)
            items.append({'itemCode': itemCode , 'quantity':od.quantity})
    actions = []
    item_data = []

    async with aiohttp.ClientSession() as session:
        for item in items:
            url = f"http://127.0.0.1:8001/inventory/{item['itemCode']}/{item['quantity']}/"
            actions.append(asyncio.ensure_future(get_validation(session, url)))

        res_item = await asyncio.gather(*actions)
        for data in res_item:
            item_data.append(data)
    
    for m in item_data:
        if m == 'NotAvailable':
            return JsonResponse("Order was not successful, some of the Items are not stocked. Please try again later", safe=False)

    total_time = time.time() - starting_time
    order.orderStatus = "Order Successfully"
    order.save()
    return JsonResponse("We have successfully processed your order", safe=False)
