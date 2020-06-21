from app_websites.models import *
from app_stats.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

def order_items(request):

    # Update Order Table by Annoting item_qty from the OrderItem Table
    ord_items = Order.objects.all().annotate(ord_items=Sum('orderitem__item_qty')).filter(pk=OuterRef('pk'))

    qs = Order.objects.annotate (
        ord_items=Subquery(ord_items.values('ord_items'), output_field=IntegerField()), 
    ).order_by('order_id')

    for i in qs: 
        i.items_qty = i.ord_items or 0
        i.save()

    return ()