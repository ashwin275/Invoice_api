from django.urls import path
from . import views
urlpatterns = [
   
    path('invoices/',views.InvoiceApiView.as_view(),name='invoice'),
    path('invoices/<int:pk>/',views.InvoiceApiView.as_view(),name='invoice-updation')
]