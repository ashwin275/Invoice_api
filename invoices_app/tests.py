from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Invoice, InvoiceDetail


class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.invoices_url = reverse('invoice')
        self.data = {
            'customer_name': 'Ashwin Raj ck',
            'description': 'Description for the invoice',
            'unit_price': 20,
            'quantity': 10
        }

        self.invoice = Invoice.objects.create(customer_name='Customer Testing')
        self.invoice_detail = InvoiceDetail.objects.create(
            invoice=self.invoice, description='Invoice Description', unit_price=20, quantity=20, price=400)

    def test_create_invoice(self):
        response = self.client.post(
            self.invoices_url, self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_invoice_list(self):
        response = self.client.get(self.invoices_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail(self):

        url = reverse('invoice-updation', kwargs={'pk': self.invoice.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_invoice(self):

        url = reverse('invoice-updation', kwargs={'pk':  self.invoice.id})
        data = {
            'customer_name': 'New Customer Name'
        }
        response = self.client.patch(url, data, format='json')
        payload = response.data['payload']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payload['customer_name'], 'New Customer Name')

    def test_delete_invoice(self):

        url = reverse('invoice-updation', kwargs={'pk': self.invoice.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
