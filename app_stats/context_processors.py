from app_websites.models import *
from app_stats.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count

def stats_sales_day(request):

    # Update the Day Table by Annotating Sales from the Order Table
    tot_order_qty = Day.objects.all().annotate(tot_order_qty=Count('order')).filter(pk=OuterRef('pk'))
    tot_item_qty = Day.objects.all().annotate(tot_item_qty=Sum('order__items_qty')).filter(pk=OuterRef('pk'))
    tot_item_price = Day.objects.all().annotate(tot_item_price=Sum('order__items_total_price')).filter(pk=OuterRef('pk'))
    tot_delivery = Day.objects.all().annotate(tot_delivery=Sum('order__delivery_price')).filter(pk=OuterRef('pk'))
    tot_vat = Day.objects.all().annotate(tot_vat=Sum('order__vat')).filter(pk=OuterRef('pk'))
    tot_revenue = Day.objects.all().annotate(tot_revenue=Sum('order__total_price_inc_vat')).filter(pk=OuterRef('pk'))

    qs = Day.objects.annotate (
        tot_order_qty=Subquery(tot_order_qty.values('tot_order_qty'), output_field=DecimalField()),
        tot_item_qty=Subquery(tot_item_qty.values('tot_item_qty'), output_field=DecimalField()),
        tot_item_price=Subquery(tot_item_price.values('tot_item_price'), output_field=DecimalField()), 
        tot_delivery=Subquery(tot_delivery.values('tot_delivery'), output_field=DecimalField()),
        tot_vat=Subquery(tot_vat.values('tot_vat'), output_field=DecimalField()),
        tot_revenue=Subquery(tot_revenue.values('tot_revenue'), output_field=DecimalField()),
    ).order_by('day')

    for i in qs:
        i.order_qty = i.tot_order_qty or 0
        i.item_qty = i.tot_item_qty or 0
        i.item_price = i.tot_item_price or 0
        i.delivery = i.tot_delivery or 0
        i.vat = i.tot_vat or 0
        i.revenue = i.tot_revenue or 0
        i.save()

    return()

# Add a Time field in Django
# Rename Day to Date in Orders table
# Remove Month and Year from Orders
# Make the Date linked to Month and month linked to year via Foreign Key
# Calculate Month based on Day
# Calculate Year based on Month
# This would reduce by thousands of queries as year would need 12 calls and month would need 30. 
# Test the speed by commenting out the two function below and run the app. 
# Add 'stats_updated' field to the orders table default to false
# Then if stats_updated = false, add the value to the totals and change to True


# Regarding the updating when required. Could have a 'last updated' field in the date table. 
# Then say if latest order date time is > last updated field run the function (could be costly updating every field).
# Or could make an update stats table, which inserts a field with a datetime everytime the stats are run.
# Install debug toolbar

# Might be easier to use a class based view
# Setup 3 new tables - Date2, Month2 and Year2
' '


def stats_sales_mon(request):

    # Update Month Table by Annotating Sales from the Order Table
    tot_order_qty = Month.objects.all().annotate(tot_order_qty=Count('order')).filter(pk=OuterRef('pk'))
    tot_item_qty = Month.objects.all().annotate(tot_item_qty=Sum('order__items_qty')).filter(pk=OuterRef('pk'))
    tot_item_price = Month.objects.all().annotate(tot_item_price=Sum('order__items_total_price')).filter(pk=OuterRef('pk'))
    tot_delivery = Month.objects.all().annotate(tot_delivery=Sum('order__delivery_price')).filter(pk=OuterRef('pk'))
    tot_vat = Month.objects.all().annotate(tot_vat=Sum('order__vat')).filter(pk=OuterRef('pk'))
    tot_revenue = Month.objects.all().annotate(tot_revenue=Sum('order__total_price_inc_vat')).filter(pk=OuterRef('pk'))

    qs = Month.objects.annotate (
        tot_order_qty=Subquery(tot_order_qty.values('tot_order_qty'), output_field=DecimalField()),
        tot_item_qty=Subquery(tot_item_qty.values('tot_item_qty'), output_field=DecimalField()),
        tot_item_price=Subquery(tot_item_price.values('tot_item_price'), output_field=DecimalField()), 
        tot_delivery=Subquery(tot_delivery.values('tot_delivery'), output_field=DecimalField()),
        tot_vat=Subquery(tot_vat.values('tot_vat'), output_field=DecimalField()),
        tot_revenue=Subquery(tot_revenue.values('tot_revenue'), output_field=DecimalField()),
        ).order_by('month_id')

    for i in qs:
        i.order_qty = i.tot_order_qty or 0
        i.item_qty = i.tot_item_qty or 0
        i.item_price = i.tot_item_price or 0
        i.delivery = i.tot_delivery or 0
        i.vat = i.tot_vat or 0
        i.revenue = i.tot_revenue or 0
        i.save()

    return ()

def stats_sales_year(request):

    # Update Month Table by Annotating Sales from the Order Table
    tot_order_qty = Year.objects.all().annotate(tot_order_qty=Sum('month__order_qty')).filter(pk=OuterRef('pk'))
    tot_item_qty = Year.objects.all().annotate(tot_item_qty=Sum('month__item_qty')).filter(pk=OuterRef('pk'))
    tot_item_price = Year.objects.all().annotate(tot_item_price=Sum('month__item_price')).filter(pk=OuterRef('pk'))
    tot_delivery = Year.objects.all().annotate(tot_delivery=Sum('month__delivery')).filter(pk=OuterRef('pk'))
    tot_vat = Year.objects.all().annotate(tot_vat=Sum('month__vat')).filter(pk=OuterRef('pk'))
    tot_revenue = Year.objects.all().annotate(tot_revenue=Sum('month__revenue')).filter(pk=OuterRef('pk'))

    qs = Year.objects.annotate (
        tot_order_qty=Subquery(tot_order_qty.values('tot_order_qty'), output_field=IntegerField()),
        tot_item_qty=Subquery(tot_item_qty.values('tot_item_qty'), output_field=IntegerField()),
        tot_item_price=Subquery(tot_item_price.values('tot_item_price'), output_field=DecimalField()), 
        tot_delivery=Subquery(tot_delivery.values('tot_delivery'), output_field=DecimalField()),
        tot_vat=Subquery(tot_vat.values('tot_vat'), output_field=DecimalField()),
        tot_revenue=Subquery(tot_revenue.values('tot_revenue'), output_field=DecimalField()),
        ).order_by('year')

    for i in qs:
        i.order_qty = i.tot_order_qty or 0
        i.item_qty = i.tot_item_qty or 0
        i.item_price = i.tot_item_price or 0
        i.delivery = i.tot_delivery or 0
        i.vat = i.tot_vat or 0
        i.revenue = i.tot_revenue or 0
        i.save()

    return ()