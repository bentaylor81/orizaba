from .models import *

def product_list(request):
    context = { 
            'product_list' : Product.objects.all(),
            }
    return ( context )