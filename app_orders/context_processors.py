from django.conf import settings
from app_products.models import *
from app_orders.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count
import pdfkit
import wkhtmltopdf

# CREATE INITIAL STATUS IN ORDERSTATUS HISTORY TABLE WHEN ORDER IS CREATED
# SET STATUS_UPDATED FIELD IN ORDER TABLE TO TRUE
def initial_status(request):
    orders = Order.objects.filter(initial_status_added=False, date__gt="2021-01-01")
    type_inst = OrderStatusType.objects.get(pk=10)

    for order in orders:
        OrderStatusHistory.objects.create(order_id=order, status_type=type_inst, date=order.date) 
        order.initial_status_added = True
        order.save()
    return()

# CREATE PDF INVOICE WHEN AN ORDER COMES IN
# SET INVOICE_CREATED FIELD IN ORDER TABLE TO TRUE   
def invoice_pdf(request):
    orders = Order.objects.filter(invoice_created=False)
    wkhtmltopdf_config = settings.WKHTMLTOPDF_CMD
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_config)

    for order in orders: 
        order.invoice_created = True  
        order.save()  
        order_id = order.order_id  
        projectUrl = 'http://' + request.get_host() + '/orders/%s/invoice' % order_id 
        # pdf = pdfkit.from_url(projectUrl, 'https://orizaba-control.s3-us-west-2.amazonaws.com/pdf/invoices/invoice-%s.pdf' % order_id, configuration=config)
        pdf = pdfkit.from_url(projectUrl, 'static/pdf/invoices/invoice-%s.pdf' % order_id, configuration=config)   # Change this to upload to S3
    return()

