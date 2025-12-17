function addToCart(id,name,price){
    fetch("api/carts", {
        method: "post",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "price": price
        }),
        headers: {
            "content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter');
        for(let e of d){
            e.innerText = data.total_quantity;
        }
    })
}

function updateCart(productId, obj){
    fetch(`api/carts/${productId}`, {
        method: "put",
        body: JSON.stringify({
            "quantity": parseInt(obj.value)
        }),
        headers: {
            "content-type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter');
        for(let e of d){
            e.innerText = data.total_quantity;
        }

        let d2 = document.getElementsByClassName('cart-amount');
        for(let e of d2){
            e.innerText = data.total_amount.toLocaleString("en");
        }
    })
}

function deleteCart(productId){
    if(confirm("Ban co chac chan xoa?")===true){
        fetch(`api/carts/${productId}`, {
        method: "delete"
    }).then(res => res.json()).then(data => {
        let d = document.getElementsByClassName('cart-counter');
        for(let e of d){
            e.innerText = data.total_quantity;
        }

        let d2 = document.getElementsByClassName('cart-amount');
        for(let e of d2){
            e.innerText = data.total_amount.toLocaleString("en");
        }

        let e = document.getElementById(`product${productId}`);
        e.style.display = "none";
    })
    }
}

function pay(){
    if(confirm("Ban co chac chan thanh toan?")===true){
        fetch("api/pay", {
        method: "post"
    }).then(res => res.json()).then(data => {
       if(data.status===200){
            location.reload();
       }else{
            alert(data.err_msg);
       }
    })
    }
}