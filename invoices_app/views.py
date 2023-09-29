from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import APIView
from rest_framework.exceptions import NotFound
from .serializers import  InvoiceDetailSerializer
from .models import Invoice, InvoiceDetail
from django.shortcuts import get_object_or_404


class InvoiceApiView(APIView):
    def post(self, request):

        try:

            if not request.data:
                return Response({
                    'error': 'no data provide',
                    'details': 'provide a valid data'
                }, status=status.HTTP_400_BAD_REQUEST)


            customer_name = request.data.get('customer_name')
            if not customer_name:
                return Response({'error': 'provide customer name'}, status=status.HTTP_400_BAD_REQUEST)

            invoice_instance = Invoice.objects.create(
                customer_name=customer_name)
           
            invoice_detail_serializer = InvoiceDetailSerializer(
                data=request.data, context={'Invoice_instance': invoice_instance})

            if invoice_detail_serializer.is_valid():
                invoice_detail_serializer.save()
                return Response({'message': 'invoice successfully created', 'payload': invoice_detail_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error':invoice_detail_serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def get(self, request, pk=None):

        try:
            if pk:  # retrieving details of a specific invoice

                try:
                    invoice_detail_instance = InvoiceDetail.objects.get(
                        invoice=pk)
                except InvoiceDetail.DoesNotExist:
                    return Response({'error': 'Invoice does not exist'}, status=status.HTTP_404_NOT_FOUND)
                serializer = InvoiceDetailSerializer(invoice_detail_instance)
                return Response({'payload': serializer.data})


            else:  # retrieving details of all invoice in the database

                invoice_detail_instances = InvoiceDetail.objects.all()
                serializer = InvoiceDetailSerializer(
                    invoice_detail_instances, many=True)
                return Response({'payload': serializer.data})
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk=None):
        try:
            if not request.data:
                return Response({
                    'error': 'no data provide',
                    'details': 'Provide a valid data'
                }, status=status.HTTP_400_BAD_REQUEST)

            if 'customer_name' in request.data:
                invoice_instance = get_object_or_404(Invoice, pk=pk)
                invoice_instance.customer_name = request.data.get(
                    'customer_name')
                invoice_instance.save()

            invoice_detail = get_object_or_404(InvoiceDetail, invoice=pk)
            serializer = InvoiceDetailSerializer(
                invoice_detail, data=request.data, partial=True)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({'message': 'invoice successfully updated', 'payload': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None):
        try:
            if not pk:
                return Response({'error': 'Provide a valid ID'}, status=status.HTTP_400_BAD_REQUEST)

            invoice_detail_instance = get_object_or_404(Invoice, pk=pk)
            invoice_detail_instance.delete()
            return Response({'message': 'Invoice successfully deleted'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
