from src.bot import *
import paypalrestsdk

paypalrestsdk.configure({
    'mode': 'live',
    'client_id': PAYPAL_CLIENT_ID,
    'client_secret': PAYPAL_CLIENT_SECRET,
})


def get_payment(payment_id):
    payment = paypalrestsdk.Payment.find(payment_id)
    logging.info(str(payment))
    logging.info(str(payment.payer))
    if payment.payer is not None:
        result = payment.transactions[0].description
        return result
    else:
        return False


def create_payment(user_id, amount, time):
    payment = paypalrestsdk.Payment({
        "intent": "sale",

        "payer": {
            "payment_method": "paypal"},

        "redirect_urls": {
            "return_url": "https://t.me/Donnerussebot",
            "cancel_url": "https://t.me/Donnerussebot"},

        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Subscription",
                    "sku": "Subscription",
                    "price": f"{amount}.00",
                    "currency": "EUR",
                    "quantity": 1}
                ]},

            "amount": {
                "total": f"{amount}.00",
                "currency": "EUR"},
            "description": f"{user_id}={amount}={time}"
        }]
    })

    if payment.create():
        result = []

        for link in payment.links:
            if link.rel == "approval_url":
                approval_url = str(link.href)
                result.append(approval_url)
        result.append(payment.id)

        return result
    else:
        return False


# payment_history = paypalrestsdk.Payment.all()
# print(payment_history)
