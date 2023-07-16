from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice

class InvoiceTests(APITestCase):
    def test_create_invoice(self):
        url = reverse('invoice-list')
        data = {
            "date": "2023-07-16",
            "invoice_no": "INV-001",
            "customer_name": "John Doe",
            "invoice_details": [
                {
                    "description": "Item 1",
                    "quantity": 2,
                    "unit_price": 10.99,
                    "price": 21.98
                },
                {
                    "description": "Item 2",
                    "quantity": 3,
                    "unit_price": 5.99,
                    "price": 17.97
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.get().invoice_no, 'INV-001')

