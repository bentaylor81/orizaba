from django.db import models

class OrderStatusHistory(models.Model):
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    status_type = models.ForeignKey('orderstatustype', db_column='status_type', on_delete=models.CASCADE, null=True, blank=True)   
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id) + ' | ' + str(self.status_type.name) + ' | ' + str(self.date)

    class Meta:
        ordering = ["-date"]

class OrderShipment(models.Model):
    orderlabel_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True) 
    delivery_firstname = models.CharField(max_length=200, blank=True)
    delivery_lastname = models.CharField(max_length=200, blank=True)
    delivery_address_1 = models.CharField(max_length=200, blank=True)
    delivery_address_2 = models.CharField(max_length=200, blank=True)
    delivery_city = models.CharField(max_length=200, blank=True)
    delivery_postcode = models.CharField(max_length=200, blank=True)
    delivery_country = models.CharField(max_length=200, blank=True)
    delivery_country_code = models.CharField(max_length=200, blank=True)
    delivery_phone = models.CharField(max_length=200, blank=True)
    delivery_email = models.CharField(max_length=200, blank=True)
    service_id = models.ForeignKey('OrderDeliveryMethod', db_column='service_id', to_field='service_id', on_delete=models.CASCADE, null=True, blank=True)
    shipping_ref = models.CharField(max_length=200, blank=True) 
    tracking_code = models.CharField(max_length=200, blank=True)
    tracking_ref = models.CharField(max_length=200, blank=True)
    total_price_ex_vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    weight = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    date_sent = models.DateField(null=True)
    date_delivered = models.DateTimeField(null=True) 

    def __str__(self):
        return str(self.order_id) + ' | ' + str(self.service_id)

    class Meta:
        ordering = ["-date_created"]

class OrderNote(models.Model):
    ordernote_id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(blank=False)
    added_by = models.CharField(max_length=10, blank=True) 
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.ordernote_id) + ' | ' + self.note + ' | ' + self.added_by + ' | ' + str(self.order_id)
       
    class Meta:
        ordering = ["-date"]


class RefundOrderItem(models.Model):
    CHOICES = [
        ('Order Item Refund', 'Order Item Refund'),
        ('Postage Refund', 'Postage Refund'),
        ('Other Refund', 'Other Refund'),
    ]
    orderitem_id = models.PositiveIntegerField(null=True, blank=True)
    refund_type = models.CharField(choices=CHOICES, max_length=200, blank=True) 
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    refundorder = models.ForeignKey('refundorder', on_delete=models.CASCADE, null=True, blank=True)
    item_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    item_qty = models.IntegerField(blank=True, default=0)
    total_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2) 
    line_description = models.CharField(max_length=200, blank=True) 
    xero_line_item = models.IntegerField(blank=True, default=0)
    stock_movement_added = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.refundorder.pk) + ' | ' + str(self.item_qty) + ' | ' + str(self.item_price)

    class Meta:
        ordering = ["xero_line_item"]

class RefundOrder(models.Model):
    CHOICES = [
        ('Customer Returned Order', 'Customer Returned Order'),
        ('Incorrect Part Sent', 'Incorrect Part Sent'),
        ('Faulty Part Refund', 'Faulty Part Refund'),
        ('Cancelled Order Refund', 'Cancelled Order Refund'),
        ('Duplicate Order Refund', 'Duplicate Order Refund'),
        ('Postage Refund Orders Combined', 'Postage Refund Orders Combined'),
        ('Postage Refund Other', 'Postage Refund Other'),
        ('Other Reason', 'Other Reason')
    ]
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    refund_amount = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2) 
    date_time = models.DateTimeField(auto_now_add=True)
    xero_credit_note = models.BooleanField(default=True) 
    sagepay_refund = models.BooleanField(default=True) 
    email_customer = models.BooleanField(default=True) 
    refund_reason = models.CharField(choices=CHOICES, max_length=200, blank=True, null=True) 
    refund_note = models.CharField(max_length=400, blank=True, null=True) 

    def __str__(self):
        return str(self.pk) + ' | ' + str(self.refund_amount) + ' | ' + str(self.order_id.pk)

    class Meta:
        ordering = ["-date_time"]

class OrderItem(models.Model):
    orderitem_id = models.IntegerField(primary_key=True)
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey('app_products.product', db_column='product_id', on_delete=models.CASCADE, null=True, blank=True)
    item_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    item_qty = models.IntegerField(blank=True, default=0) 
    send_qty = models.IntegerField(blank=True, default=0) 
    refunded_qty = models.IntegerField(blank=True, default=0) 
    total_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    stock_movement_added = models.BooleanField(default=False) # Set this to True when going live, so the stock doesn't get updated for all previous orders.
    item_refunded = models.BooleanField(default=False) 

    def __str__(self):
        return str(self.orderitem_id) + ' | ' + str(self.item_qty) + ' | ' + str(self.send_qty)

    class Meta:
        ordering = ["-order_id__date", "orderitem_id", "-send_qty"]

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_no = models.IntegerField(blank=True)
    billing_firstname = models.CharField(max_length=200, blank=True)  
    billing_lastname = models.CharField(max_length=200, blank=True)  
    billing_address_1 = models.CharField(max_length=200, blank=True)
    billing_address_2 = models.CharField(max_length=200, blank=True)
    billing_city = models.CharField(max_length=200, blank=True)
    billing_postcode = models.CharField(max_length=200, blank=True)
    billing_country = models.CharField(max_length=200, blank=True)
    billing_email = models.ForeignKey('app_products.customer', to_field='billing_email', db_column='billing_email', on_delete=models.CASCADE, blank=True, null=True)
    billing_phone = models.CharField(max_length=200, blank=True)
    delivery_firstname = models.CharField(max_length=200, blank=True) 
    delivery_lastname = models.CharField(max_length=200, blank=True) 
    delivery_address_1 = models.CharField(max_length=200, blank=True)
    delivery_address_2 = models.CharField(max_length=200, blank=True)
    delivery_city = models.CharField(max_length=200, blank=True)
    delivery_postcode = models.CharField(max_length=200, blank=True)
    delivery_country = models.CharField(max_length=200, blank=True)
    delivery_country_code = models.CharField(max_length=5, blank=True)
    delivery_email = models.CharField(max_length=200, blank=True)
    delivery_phone = models.CharField(max_length=200, blank=True)
    delivery_type = models.CharField(max_length=200, blank=True)
    delivery_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    items_total_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    item_qty = models.IntegerField(blank=True, default=0)
    total_price_ex_vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2) # items_total_price + delivery_price
    vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    total_price_inc_vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    website = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    sagepay_tx_code = models.CharField(max_length=200, blank=True)
    status_current = models.ForeignKey('orderstatustype', db_column='status_current', on_delete=models.CASCADE, blank=True, null=True, default='10') 
    # BOOLEAN FLAG AND RETURN FIELDS
    initial_status_added = models.BooleanField(default=False) # Used to update the initial status
    return_order = models.BooleanField(default=False) # This put the order into the returns page table
    item_received = models.BooleanField(default=False)
    item_received_date = models.DateTimeField(null=True, blank=True)
    inspection_passed = models.BooleanField(default=False)
    inspection_passed_date = models.DateTimeField(null=True, blank=True)
    item_refunded = models.BooleanField(default=False)
    item_refunded_date = models.DateTimeField(null=True, blank=True)
    amount_refunded = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2) 
    return_complete = models.BooleanField(default=False)
    invoice_created = models.BooleanField(default=True) 
    
    def __str__(self):
        return str(self.date) + ' | ' + str(self.order_no) + ' | ' + str(self.billing_firstname) + ' ' + str(self.billing_lastname) +  ' | ' + str(self.billing_email) + ' | ' + str(self.total_price_inc_vat)

    class Meta:
        ordering = ["-date"]

class OrderStatusType(models.Model):
    status = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=200, blank=True)
    icon_color = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.status) + ' | ' + str(self.name)

    class Meta:
        ordering = ["status"]

class OrderDeliveryMethod(models.Model):
    CHOICES = [
        ('APC', 'APC'),
        ('DPD', 'DPD'),
        ('Royal Mail', 'Royal Mail'),
        ('NA', 'NA'),
    ]
    delivery_method = models.CharField(max_length=200, blank=True)
    courier = models.CharField(choices=CHOICES, max_length=200, blank=True)
    service_id = models.IntegerField(blank=True, null=True, unique=True)
    sort_order = models.IntegerField(default=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.delivery_method + ' | ' + str(self.courier) + ' | ' + str(self.service_id)

    class Meta:
        ordering = ["sort_order"]
