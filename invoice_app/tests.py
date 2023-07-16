from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Invoice, InvoiceDetail

class InvoiceTests(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(
            date="2023-07-16",
            invoice_no="INV-001",
            customer_name="John Doe"
        )
        self.invoice_detail1 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description="Item 1",
            quantity=2,
            unit_price=10.99,
            price=21.98
        )
        self.invoice_detail2 = InvoiceDetail.objects.create(
            invoice=self.invoice,
            description="Item 2",
            quantity=3,
            unit_price=5.99,
            price=17.97
        )

    def test_get_invoices(self):
        url = reverse('invoice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_invoice(self):
        url = reverse('invoice-detail', args=[self.invoice.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_no'], 'INV-001')
        self.assertEqual(len(response.data['invoice_details']), 2)

    def test_create_invoice(self):
        url = reverse('invoice-list')
        data = {
            "date": "2023-07-17",
            "invoice_no": "INV-002",
            "customer_name": "Jane Smith",
            "invoice_details": [
                {
                    "description": "Item 3",
                    "quantity": 1,
                    "unit_price": 9.99,
                    "price": 9.99
                }
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        self.assertEqual(InvoiceDetail.objects.count(), 3)

    def test_update_invoice(self):
        url = reverse('invoice-detail', args=[self.invoice.id])
        data = {
            "date": "2023-07-16",
            "invoice_no": "INV-001-updated",
            "customer_name": "John Doe",
            "invoice_details": [
                {
                    "id": self.invoice_detail1.id,
                    "description": "Item 1 - updated",
                    "quantity": 3,
                    "unit_price": 10.99,
                    "price": 32.97
                },
                {
                    "id": self.invoice_detail2.id,
                    "description": "Item 2 - updated",
                    "quantity": 4,
                    "unit_price": 5.99,
                    "price": 23.96
                }
            ]
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_no'], 'INV-001-updated')
        self.assertEqual(len(response.data['invoice_details']), 2)
        self.assertEqual(response.data['invoice_details'][0]['description'], 'Item 1 - updated')
        self.assertEqual(response.data['invoice_details'][0]['quantity'], 3)
        self.assertEqual(response.data['invoice_details'][1]['description'], 'Item 2 - updated')
        self.assertEqual(response.data['invoice_details'][1]['quantity'], 4)

    def test_delete_invoice(self):
        url = reverse('invoice-detail', args=[self.invoice.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
