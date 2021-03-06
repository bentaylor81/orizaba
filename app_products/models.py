from django.db import models
import datetime

class MagentoProductSync(models.Model):
    product = models.ForeignKey('product', on_delete=models.CASCADE, null=True, blank=True)
    stock_qty = models.IntegerField(blank=True, default=0)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)  
    date_synced = models.DateTimeField(blank=True, null=True) 
    has_synced = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.product)

    class Meta:
        ordering = ["-has_synced", "pk"]

class StockCheck(models.Model):
    product = models.ForeignKey('product', on_delete=models.CASCADE, null=True, blank=True)
    expected_qty = models.IntegerField(blank=True, default=0)
    actual_qty = models.IntegerField(blank=True, default=0)
    difference_qty = models.IntegerField(blank=True, default=0)
    date_checked = models.DateTimeField(auto_now_add=True, blank=True, null=True) 

    def __str__(self):
        return str(self.id) + ' | ' + str(self.product)

    class Meta:
        ordering = ["-id"]

class StockLocation(models.Model):
    product = models.ForeignKey('product', on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True) 

    def __str__(self):
        return str(self.id) + ' | ' + str(self.product)

    class Meta:
        ordering = ["-id"]

class StockMovement(models.Model):
    STATUS_CHOICES = [
        ('Online Sale', 'Online Sale'),
        ('Purchase Order Receipt', 'Purchase Order Receipt'),
        ('Manual Adjustment', 'Manual Adjustment'),      
    ]
    product = models.ForeignKey('product', on_delete=models.CASCADE, null=True, blank=True)
    adjustment_qty = models.IntegerField(blank=True, default=0) # Related to the quantity delivered, like in PurchaseOrderItem table
    movement_type = models.CharField(max_length=200, choices=STATUS_CHOICES, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True) 
    purchaseorder = models.ForeignKey('purchaseorder', on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.ForeignKey('app_orders.order', db_column='order_id', on_delete=models.CASCADE, null=True, blank=True)
    current_stock_qty = models.IntegerField(default=0, blank=True, null=True)
    comments = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.product_id) + ' | ' + self.product.product_name + ' | ' + str(self.date_added) + ' | ' + str(self.adjustment_qty) + ' | ' + str(self.current_stock_qty) + ' | ' + str(self.movement_type) + ' | ' + str(self.purchaseorder)

    class Meta:
        ordering = ["-date_added", "-pk"]

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
    order_qty = models.IntegerField(blank=True, default=0)      
    received_qty = models.IntegerField(blank=True, default=0)   
    outstanding_qty = models.IntegerField(blank=True, default=0)    
    received_status = models.CharField(max_length=200, choices=STATUS_CHOICES, blank=True, default="Order Pending") 
    comments = models.CharField(max_length=100, blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.purchaseorder.reference) + ' | ' + str(self.product.product_name) + ' | ' + str(self.order_qty) + ' | ' + str(self.received_qty) + ' | ' + str(self.outstanding_qty) + ' | ' + str(self.received_status)

    class Meta:
        ordering = ["product_sku", "-id"]

class PurchaseOrder(models.Model):
    PO_CHOICES = [
        ('Pending', 'Pending'),
        ('Part Receipt', 'Part Receipt'),
        ('Complete', 'Complete'),
    ]
    po_id = models.AutoField(primary_key=True)
    reference = models.CharField(max_length=200, blank=True)	
    supplier_reference = models.CharField(max_length=200, blank=True)	
    supplier = models.ForeignKey('supplier', db_column='supplier', on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    date_ordered = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=200, choices=PO_CHOICES, blank=True)
    notes = models.CharField(max_length=1000, blank=True)
    total_lines = models.IntegerField(blank=True, default=0)
    order_qty = models.IntegerField(blank=True, default=0)      
    received_qty = models.IntegerField(blank=True, default=0) 
    outstanding_qty = models.IntegerField(blank=True, default=0)    

    def __str__(self):
        return str(self.po_id) + ' | ' + str(self.reference)

    class Meta:
        ordering = ["-pk"]

class ProductLabel(models.Model):
    product = models.ForeignKey('product', on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField(blank=True)
    is_printed = models.BooleanField(default=False)
    date_printed = models.DateTimeField(blank=True, null=True) 

    def __str__(self):
        return str(self.product) + ' | ' + str(self.qty) + ' | ' + str(self.date_printed)

    class Meta:
        ordering = ["id"]

class Product(models.Model):
    TYPE_CHOICES = [
        ('Part', 'Part'),
        ('Delivery', 'Delivery'),
        ('Gift', 'Gift'),
    ]
    STATUS_CHOICES = [
        ('Enabled', 'Enabled'),
        ('Disabled', 'Disabled'),
    ]
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=200, blank=True)	
    product_type = models.CharField(max_length=200, blank=True, choices=STATUS_CHOICES, default='Part')	
    sku = models.CharField(max_length=200, blank=True)
    buy_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    sell_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    stock_qty = models.IntegerField(blank=True, default=0) # Will be removed
    orizaba_stock_qty = models.IntegerField(blank=True, default=0) # Will eventually be changed to stock_qty
    last_stock_check = models.DateTimeField(blank=True, null=True)
    item_profit = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    stock_profit = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    buy_value = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    sell_value = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)  
    profit_margin = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)    
    weight = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=4)
    location = models.CharField(max_length=200, blank=True, null=True)	
    part_type = models.CharField(max_length=200, blank=True, default='null')	
    brand = models.ForeignKey('brand', db_column='brand', on_delete=models.CASCADE, null=True, blank=True, default='Other')
    supplier = models.ForeignKey('supplier', db_column='supplier', on_delete=models.CASCADE, null=True, blank=True, default='Unknown')
    url = models.CharField(max_length=200, blank=True, default='null')
    status = models.CharField(max_length=200, blank=True, choices=STATUS_CHOICES, default='Enabled')	
    has_image = models.BooleanField(default=False) 
    product_image = models.ImageField(upload_to="images/products", null=True, blank=True)
    condition = models.CharField(max_length=200, blank=True, default='new')	
    special_order = models.CharField(max_length=200, blank=True, default='no')	
    sealed_item = models.BooleanField(default=False)

    def __str__(self):
        return str(self.sku)

    class Meta:
        ordering = ["product_id", "location"]

    @property
    def product_calcs(self, *args, **kwargs):
        # Calculate - Buy Value, Sell Value, Profit Per Item, Total Stock Profit
        self.buy_value = (self.buy_price * self.stock_qty)
        self.sell_value = (self.sell_price * self.stock_qty)
        self.item_profit = (self.sell_price - self.buy_price)
        self.stock_profit = (self.sell_value - self.buy_value)
        # Calculate the Profit Margin on the item
        if self.sell_price != 0:
            profit = ((self.item_profit / self.sell_price) * 100) 
            self.profit_margin = round(profit, 0)
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

