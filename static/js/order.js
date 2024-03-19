var updateBtns = document.getElementsByClassName('update-order')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var itemId = this.dataset.item
		var action = this.dataset.action
		console.log('itemId:', itemId, 'Action:', action)
		console.log('USER:', user)
		updateUserOrder(itemId, action)
		
	})
}

function updateUserOrder(itemId, action){
	console.log('User is authenticated, sending data...')

		var url = '/order/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			}, 
			body:JSON.stringify({'itemId':itemId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}

function addCookieItem(itemId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (order[itemId] == undefined){
		order[itemId] = {'quantity':1}

		}else{
			order[itemId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		order[itemId]['quantity'] -= 1

		if (order[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete order[itemId];
		}
	}
	console.log('ORDER:', order)
	document.cookie ='order=' + JSON.stringify(order) + ";domain=;path=/"
	
	location.reload()
}