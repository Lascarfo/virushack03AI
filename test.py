
from telebot.types import LabeledPrice, ShippingOption

pickup = ShippingOption(id='first', title='pickup')
pickup.add_price(LabeledPrice('count', 100))
pickup = obj.to_json()
print(obj)

shipping_options = [pickup]


print(shipping_options)