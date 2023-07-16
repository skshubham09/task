from rest_framework import serializers
from .models import Invoice, InvoiceDetail

class InvoiceDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetail
        fields = ['description', 'quantity', 'unit_price', 'price']

class InvoiceSerializer(serializers.ModelSerializer):
    invoice_details = InvoiceDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ['date', 'invoice_no', 'customer_name', 'invoice_details']

    def create(self, validated_data):
        invoice_details_data = validated_data.pop('invoice_details')
        invoice = Invoice.objects.create(**validated_data)
        for detail_data in invoice_details_data:
            InvoiceDetail.objects.create(invoice=invoice, **detail_data)
        return invoice
