from rest_framework import serializers
from .models import InvoiceDetail


class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = "__all__"
        read_only_fields = ['invoice', 'price']

    def create(self, validated_data):
        validated_data['invoice'] = self.context.get('Invoice_instance')
        validated_data['price'] = validated_data.get(
            'quantity') * validated_data.get('unit_price')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'quantity' or 'unit_price' in validated_data:
            validated_data['price'] = validated_data.get(
                'quantity', instance.quantity) * validated_data.get('unit_price', instance.unit_price)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        invoice_instance = instance.invoice
        data['customer_name'] = invoice_instance.customer_name if invoice_instance else None
        data['Date'] = invoice_instance.date if invoice_instance else None
        data['id'] = invoice_instance.id if invoice_instance else None
        data.pop('invoice')
        return data
