import json
from .models import *

def cookieOrder(request):

	#Create empty orderr for now for non-logged in user
	try:
		currentorder= json.loads(request.COOKIES['order'])
	except:
	    currentorder = {}

	items = []
	order = {'get_order_items':0, 'order_status':'NotProcessed'}
	orderItems = order['get_order_items']

	for i in currentorder:
		#We use try block to prevent items in cart that may have been removed from causing error
		try:
			orderItems += currentorder[i]['quantity']

			orderItem = OrderItem.objects.get(id=i)
			

			
			order['get_order_items'] += currentorder[i]['quantity']

			item = {
				'id':orderItem.id,
				'quantity':currentorde[i]['quantity'],
				'name':orderItem.name,
				}
			items.append(item)

		except:
			pass
			
	return {'orderItems':orderItems ,'order':order, 'items':items}

def orderData(request):
	if request.user.is_authenticated:
		customer = request.user.orderclient
		order, created = Order.objects.get_or_create(orderClient=customer, orderStatus='NotProcessed')
		items = order.orderitem_set.all()
		orderItems = order.getNumberOfitems
	else:
		cookieData = cookieOrder(request)
		orderItems = cookieData['orderItems']
		order = cookieData['order']
		items = cookieData['items']

	return {'orderItems':orderItems ,'order':order, 'items':items}

