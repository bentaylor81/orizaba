from django.conf import settings
from app_products.models import *
from app_orders.models import *
from .views import *
import wkhtmltopdf
import pdfkit

def generate_pdf():
    print('Hello Ben')
   