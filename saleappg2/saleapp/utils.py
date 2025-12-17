def count_cart(cart):
    total_quantity, total_amount = 0,0

    if cart:
        for p in cart.values():
            total_quantity += p["quantity"]
            total_amount += p["quantity"]*p["price"]

    return {
        "total_quantity": total_quantity,
        "total_amount": total_amount
    }