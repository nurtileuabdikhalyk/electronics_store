var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)

		if (user == 'AnonymousUser'){
		   console.log('User',user)
		    addCookieItem(productId, action)
		}
		else{

            updateUserOrder(productId, action)
       }
	})
}
function addCookieItem(productId,action){
    if (action == 'add'){
        if(cart[productId] == undefined){

            cart[productId] = {'quantity':1}
        }
        else{
            cart[productId]['quantity'] += 1
        }
    }
    if (action == 'remove'){

        cart[productId]['quantity'] -= 1
        if (cart[productId]['quantity'] <=0){
            console.log('Remove Item')
            delete cart[productId]
        }
    }
    console.log('cart:',cart)
    document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
}
function updateUserOrder(productId,action){
    var url='/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
       return response.json();
    })
    .then((data) => {
        console.log('data:',data)
    });
}