from django.db import models

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
    product_id = models.ForeignKey('product', db_column='product_id', on_delete=models.CASCADE, null=True, blank=True)
    item_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    item_qty = models.IntegerField(blank=True, default=0) 
    total_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.order_id) + ' | ' + str(self.item_qty) + ' | ' + str(self.order_id.year)

    class Meta:
        ordering = ["order_id"]

class Order(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_no = models.IntegerField(blank=True)
    billing_name = models.CharField(max_length=200, blank=True) 
    billing_address_1 = models.CharField(max_length=200, blank=True)
    billing_address_2 = models.CharField(max_length=200, blank=True)
    billing_city = models.CharField(max_length=200, blank=True)
    billing_postcode = models.CharField(max_length=200, blank=True)
    billing_country = models.CharField(max_length=200, blank=True)
    billing_email = models.ForeignKey('Customer', to_field='billing_email', db_column='billing_email', on_delete=models.CASCADE, blank=True, null=True)
    billing_phone = models.CharField(max_length=200, blank=True)
    delivery_name = models.CharField(max_length=200, blank=True)
    delivery_address_1 = models.CharField(max_length=200, blank=True)
    delivery_address_2 = models.CharField(max_length=200, blank=True)
    delivery_city = models.CharField(max_length=200, blank=True)
    delivery_postcode = models.CharField(max_length=200, blank=True)
    delivery_country = models.CharField(max_length=200, blank=True)
    delivery_email = models.CharField(max_length=200, blank=True)
    delivery_phone = models.CharField(max_length=200, blank=True)
    delivery_method = models.CharField(max_length=200, blank=True)
    delivery_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    items_total_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    total_price_ex_vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2) # items_total_price + delivery_price
    vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    total_price_inc_vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    courier = models.CharField(max_length=100, blank=True)
    ip_address = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=False)
    month = models.ForeignKey('month', db_column='month', to_field='month_id', on_delete=models.CASCADE, blank=True, null=True) 
    year = models.ForeignKey('Year', db_column='year', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.order_no) + ' | ' + str(self.billing_name) + ' | ' + str(self.year) + ' | ' + str(self.total_price_inc_vat)

    class Meta:
        ordering = ["-date"]

    @property
    def courier_func(self, *args, **kwargs):
        if self.delivery_country == "United Kingdom":
            self.courier_name = "APC"
        else:
            self.courier_name = "DPD"
        self.courier = self.courier_name
        super(Order, self).save(*args, **kwargs)
        return self.courier

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    billing_email = models.CharField(max_length=200, blank=True, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.billing_email) + ' | ' + str(self.date)

    class Meta:
        ordering = ["-date"]

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=200, blank=True)	
    sku = models.CharField(max_length=200, blank=True)
    buy_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    sell_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    stock_qty = models.IntegerField(blank=True, default=0) 
    item_profit = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    stock_profit = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    buy_value = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    sell_value = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)  
    profit_margin = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)    
    weight = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=4)
    location = models.CharField(max_length=200, blank=True)	
    brand = models.ForeignKey('brand', db_column='brand', on_delete=models.CASCADE, null=True, blank=True, default='Other')
    supplier = models.ForeignKey('supplier', db_column='supplier', on_delete=models.CASCADE, null=True, blank=True, default='Unknown')
    url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.product_id) + ' | ' + str(self.sku) + ' | ' + str(self.product_name) + ' | ' + str(self.brand)

    class Meta:
        ordering = ["product_id"]

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
        ordering = ["supplier"]

class Brand(models.Model):
    brand = models.CharField(max_length=200, primary_key=True)
    path = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.brand

    class Meta:
        ordering = ["brand"]

class Month(models.Model):
    month_id = models.IntegerField(primary_key=True)
    month = models.CharField(max_length=200, blank=True)
    year = models.ForeignKey('year', db_column='year', on_delete=models.CASCADE, null=True, blank=True, default=0)

    def __str__(self):
        return str(self.month_id) + ' | ' + str(self.month) + ' | ' + str(self.year)

class Year(models.Model):
    year = models.IntegerField(primary_key=True)

    def __str__(self):
        return str(self.year)

