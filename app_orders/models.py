from django.db import models

class OrderStatusHistory(models.Model):
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    status_type = models.ForeignKey('orderstatustype', db_column='status_type', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id.order_id) + ' | ' + str(self.order_id.billing_name) + ' | ' + str(self.status_type.name) + ' | ' + str(self.date)

    class Meta:
        ordering = ["-date"]

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

class OrderItem(models.Model):
    orderitem_id = models.IntegerField(primary_key=True)
    order_id = models.ForeignKey('order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey('app_websites.product', db_column='product_id', on_delete=models.CASCADE, null=True, blank=True)
    item_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    item_qty = models.IntegerField(blank=True, default=0) 
    send_qty = models.IntegerField(blank=True, default=0) 
    send_qty_init_updated = models.BooleanField(default=False)
    total_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.order_id) + ' | ' + str(self.item_qty)

    class Meta:
        ordering = ["-order_id", "-send_qty"]

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_no = models.IntegerField(blank=True)
    billing_name = models.CharField(max_length=200, blank=True) 
    billing_address_1 = models.CharField(max_length=200, blank=True)
    billing_address_2 = models.CharField(max_length=200, blank=True)
    billing_city = models.CharField(max_length=200, blank=True)
    billing_postcode = models.CharField(max_length=200, blank=True)
    billing_country = models.CharField(max_length=200, blank=True)
    billing_email = models.ForeignKey('app_websites.customer', to_field='billing_email', db_column='billing_email', on_delete=models.CASCADE, blank=True, null=True)
    billing_phone = models.CharField(max_length=200, blank=True)
    delivery_name = models.CharField(max_length=200, blank=True)
    delivery_address_1 = models.CharField(max_length=200, blank=True)
    delivery_address_2 = models.CharField(max_length=200, blank=True)
    delivery_city = models.CharField(max_length=200, blank=True)
    delivery_postcode = models.CharField(max_length=200, blank=True)
    delivery_country = models.CharField(max_length=200, blank=True)
    delivery_email = models.CharField(max_length=200, blank=True)
    delivery_phone = models.CharField(max_length=200, blank=True)
    delivery_method = models.ForeignKey('orderdeliverymethod', db_column='delivery_method', default=1, on_delete=models.CASCADE, blank=True, null=True)
    delivery_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    items_total_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    item_qty = models.IntegerField(blank=True, default=0)
    total_price_ex_vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2) # items_total_price + delivery_price
    vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    total_price_inc_vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    ip_address = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    time = models.TimeField(auto_now=False, auto_now_add=False, default='00:00:00')
    date = models.ForeignKey('app_stats.day', db_column='date', to_field='day', on_delete=models.CASCADE, blank=True, null=True)  
    status_current = models.ForeignKey('orderstatustype', db_column='status_current', on_delete=models.CASCADE, blank=True, null=True)
    status_updated = models.BooleanField(default=False)
    stats_updated = models.BooleanField(default=False)

    def __str__(self):
        return str(self.date) + ' | ' + str(self.order_no) + ' | ' + str(self.billing_name) + ' | ' + str(self.total_price_inc_vat)

    class Meta:
        ordering = ["-date", "-time"]

class OrderStatusType(models.Model):
    status = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True)
    icon = models.CharField(max_length=200, blank=True)
    icon_color = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.status) + ' | ' + str(self.name)

    class Meta:
        ordering = ["status"]

class OrderNavTab(models.Model):
    tab_name = models.CharField(max_length=200, blank=True)
    path = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=100)

    def __str__(self):
        return str(self.sort_order) + ' | ' + self.tab_name + ' | ' + self.path 

    class Meta:
        ordering = ["sort_order", "tab_name"]

class OrderDeliveryMethod(models.Model):
    delivery_method = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=100)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.delivery_method

    class Meta:
        ordering = ["sort_order"]
