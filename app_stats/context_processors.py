from decimal import Decimal
from django.shortcuts import render, redirect
from app_websites.models import *
from app_stats.models import *
from django.db.models import Subquery, OuterRef, DecimalField, IntegerField, Sum, Count, Q

def stats_sales_day(request):

    # Update the Day Table by Annotating Sales from the Order Table
    tot_item_qty = Day.objects.all().annotate(tot_item_qty=Sum('order__item_qty')).filter(pk=OuterRef('pk'), order__stats_updated=False)
    tot_order_qty = Day.objects.all().annotate(tot_order_qty=Count('order')).filter(pk=OuterRef('pk'), order__stats_updated=False)
    tot_item_price = Day.objects.all().annotate(tot_item_price=Sum('order__items_total_price')).filter(pk=OuterRef('pk'), order__stats_updated=False)
    tot_delivery = Day.objects.all().annotate(tot_delivery=Sum('order__delivery_price')).filter(pk=OuterRef('pk'), order__stats_updated=False)
    tot_vat = Day.objects.all().annotate(tot_vat=Sum('order__vat')).filter(pk=OuterRef('pk'), order__stats_updated=False)
    tot_revenue = Day.objects.all().annotate(tot_revenue=Sum('order__total_price_inc_vat')).filter(pk=OuterRef('pk'), order__stats_updated=False)

    qs = Day.objects.annotate (
        tot_item_qty=Subquery(tot_item_qty.values('tot_item_qty'), output_field=IntegerField()),
        tot_order_qty=Subquery(tot_order_qty.values('tot_order_qty'), output_field=IntegerField()),
        tot_item_price=Subquery(tot_item_price.values('tot_item_price'), output_field=DecimalField()),
        tot_delivery=Subquery(tot_delivery.values('tot_delivery'), output_field=DecimalField()),
        tot_vat=Subquery(tot_vat.values('tot_vat'), output_field=DecimalField()),
        tot_revenue=Subquery(tot_revenue.values('tot_revenue'), output_field=DecimalField()),
    ).order_by('day')

    for i in qs:
        i.order_qty = i.tot_order_qty or 0
        i.item_qty = i.tot_item_qty or 0
        i.item_price = i.item_price or 0
        i.delivery = i.tot_delivery or 0
        i.vat = i.tot_vat or 0
        i.revenue = i.tot_revenue or 0
        i.save()

    return()

def stats_sales_mon(request):

    # Update Month Table by Annotating Sales from the Day Table
    tot_item_qty = Month.objects.all().annotate(tot_item_qty=Sum('day__item_qty')).filter(pk=OuterRef('pk'))
    tot_order_qty = Month.objects.all().annotate(tot_order_qty=Sum('day__order_qty')).filter(pk=OuterRef('pk'))
    tot_item_price = Month.objects.all().annotate(tot_item_price=Sum('day__item_price')).filter(pk=OuterRef('pk'))
    tot_delivery = Month.objects.all().annotate(tot_delivery=Sum('day__delivery')).filter(pk=OuterRef('pk'))
    tot_vat = Month.objects.all().annotate(tot_vat=Sum('day__vat')).filter(pk=OuterRef('pk'))
    tot_revenue = Month.objects.all().annotate(tot_revenue=Sum('day__revenue')).filter(pk=OuterRef('pk'))

    qs = Month.objects.annotate (
        tot_item_qty=Subquery(tot_item_qty.values('tot_item_qty'), output_field=DecimalField()),
        tot_order_qty=Subquery(tot_order_qty.values('tot_order_qty'), output_field=DecimalField()),
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

    return()

