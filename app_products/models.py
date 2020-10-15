from django.db import models
import datetime

class StockMovement(models.Model):
    STATUS_CHOICES = [
        ('Online Sale', 'Online Sale'),
        ('Purchase Order Receipt', 'Purchase Order Receipt'),
        ('Manual Adjustment', 'Manual Adjustment'),      
    ]
    product_id = models.ForeignKey('product', on_delete=models.CASCADE, null=True, blank=True)
    adjustment_qty = models.IntegerField(blank=True, default=0) # Related to the quantity delivered, like in PurchaseOrderItem table
    movement_type = models.CharField(max_length=200, choices=STATUS_CHOICES, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True) 
    purchaseorder = models.ForeignKey('purchaseorder', on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.ForeignKey('app_orders.order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    current_stock_qty = models.IntegerField(default=0, blank=True, null=True)
    # Make a stock total added boolean field so that only future stats are counted in the stock value

    def __str__(self):
        return str(self.product_id) + ' | ' + self.product_id.product_name + ' | ' + str(self.date_added) + ' | ' + str(self.adjustment_qty) + ' | ' + str(self.current_stock_qty)

    class Meta:
        ordering = ["-date_added"]

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    billing_email = models.CharField(max_length=200, blank=True, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.billing_email) + ' | ' + str(self.date)

    class Meta:
        ordering = ["-date"]

class PurchaseOrderItem(models.Model):
    STATUS_CHOICES = [
        ('Order Pending', 'Order Pending'),
        ('Partial Receipt', 'Partial Receipt'),
        ('Full Receipt', 'Full Receipt'),
    ]
    product = models.ForeignKey('product', on_delete=models.CASCADE)
    product_sku = models.CharField(max_length=200, blank=True)
    purchaseorder = models.ForeignKey('purchaseorder', on_delete=models.CASCADE, null=True, blank=True)
    order_qty = models.IntegerField(blank=True, default=0)      # Total order quantity
    received_qty = models.IntegerField(blank=True, default=0)   # Total parts received
    outstanding_qty = models.IntegerField(blank=True, default=0)    # Total parts still outstanding
    delivery_qty = models.IntegerField(blank=True, default=0) # Parts received in this delivery
    received_status = models.CharField(max_length=200, choices=STATUS_CHOICES, blank=True, default="Order Pending") 
    status_ordering = models.IntegerField(blank=True, default=1) 
    comments = models.CharField(max_length=100, blank=True)
    label = models.BooleanField(default=False)
    date_updated = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.purchaseorder.reference) + ' | ' + str(self.product.product_name) + ' | ' + str(self.order_qty) + ' | ' + str(self.received_qty) + ' | ' + str(self.outstanding_qty) + ' | ' + str(self.received_status)

    def save(self, *args, **kwargs):
        self.received_qty = (self.received_qty + self.delivery_qty) # Delivery part added to current received value
        self.delivery_qty = 0                                       # Delivery set back to 0
        self.label = False                                          # Reset the print label to False
        self.outstanding_qty = (self.order_qty - self.received_qty) # Outstanding part qty updated

        if self.outstanding_qty == 0:
            self.received_status = 'Full Receipt'
            self.status_ordering = '3'
        elif self.outstanding_qty != 0 and self.outstanding_qty < self.order_qty:
            self.received_status = 'Partial Receipt'
            self.status_ordering = '2'
        super(PurchaseOrderItem, self).save(*args, **kwargs) 

    class Meta:
        ordering = ["-date_updated", "-id"]    # Temporarily it is not ordering by Status, so status_ordering field might not be needed.

class PurchaseOrder(models.Model):
    PO_CHOICES = [
        ("Pending", 'Pending'),
        ("Part Receipt", 'Part Receipt'),
        ("Unleashed", 'Unleashed'),
        ("Complete", 'Complete'),
    ]
    po_id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=200, blank=True)	
    supplier_reference = models.CharField(max_length=200, blank=True)	
    supplier = models.ForeignKey('supplier', db_column='supplier', on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_ordered = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=200, choices=PO_CHOICES, blank=True)
    notes = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return str(self.po_id) + ' | ' + str(self.reference)

    class Meta:
        ordering = ["-pk"]

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=200, blank=True)	
    sku = models.CharField(max_length=200, blank=True)
    buy_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    sell_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    stock_qty = models.IntegerField(blank=True, default=0) 
    orizaba_stock_qty = models.IntegerField(blank=True, default=0)
    item_profit = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    stock_profit = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    buy_value = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    sell_value = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)  
    profit_margin = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)    
    weight = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=4)
    location = models.CharField(max_length=200, blank=True, default='null')	
    part_type = models.CharField(max_length=200, blank=True, default='null')	
    brand = models.ForeignKey('brand', db_column='brand', on_delete=models.CASCADE, null=True, blank=True, default='Other')
    supplier = models.ForeignKey('supplier', db_column='supplier', on_delete=models.CASCADE, null=True, blank=True, default='Unknown')
    url = models.CharField(max_length=200, blank=True, default='null')
    image = models.CharField(max_length=200, blank=True, default='null')
    product_image = models.ImageField(upload_to="images/products", default="img/no-image.png", null=True, blank=True)
    condition = models.CharField(max_length=200, blank=True, default='new')	
    special_order = models.CharField(max_length=200, blank=True, default='no')	
    sealed_item = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sku)

    class Meta:
        ordering = ["product_id", "location"]

    @property
    def product_calcs(self, *args, **kwargs):
        if self.buy_value != (self.buy_price * self.stock_qty):
            self.buy_value = (self.buy_price * self.stock_qty)
            self.sell_value = (self.sell_price * self.stock_qty)
            self.item_profit = (self.sell_price - self.buy_price)
            self.stock_profit = (self.item_profit * self.stock_qty)
            if self.sell_price != 0:
                profit = ((self.item_profit / self.sell_price) * 100)
                profit = round(profit, 0)
                self.profit_margin = profit
            else:
                self.profit_margin = 0
            super(Product, self).save(*args, **kwargs)
        return ''

class Supplier(models.Model):
    supplier = models.CharField(max_length=200, primary_key=True)
    path = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=100)

    def __str__(self):
        return self.supplier

    class Meta:
        ordering = ["sort_order"]

class Brand(models.Model):
    brand = models.CharField(max_length=200, primary_key=True)
    path = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.brand

    class Meta:
        ordering = ["brand"]

