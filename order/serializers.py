from rest_framework import serializers
from order.models import Order
from order.send_mail import send_order_confirmation_code

class OrderSerializer(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)

    class Meta:
        model = Order
        fields = '__all__'
    
    def create(self, validated_data):
        amount = validated_data.get('amount') # 200
        product = validated_data.get('product') # p1

        if amount >  product.amount: # 200 > 10
            raise serializers.ValidationError('нет такого количества')
        if amount == 0:
            raise serializers.ValidationError('необходимо заказать минимум один товар!')
        
        product.amount -= amount
        product.save(update_fields=['amount'])
        
        order = Order.objects.create(**validated_data) # amout product

        send_order_confirmation_code(order.owner.email, order.activation_code, order.product.title, order.total_price)

        return order
        
