from django.db import models

# Create your models here.


class Invoice(models.Model):
    customer_name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Invoice #{self.id} - {self.customer_name}"


class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice,related_name='invoice_details',on_delete=models.CASCADE)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10,decimal_places=2)
    price = models.DecimalField(max_digits=10 , decimal_places=2)


    def __str__(self) -> str:
        return f"Invoice Detail #{self.invoice.id}"