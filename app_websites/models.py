from django.db import models

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
    image = models.CharField(max_length=200, blank=True, default='null')
    condition = models.CharField(max_length=200, blank=True, default='new')	
    special_order = models.CharField(max_length=200, blank=True, default='no')	

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

class NavigationOrderTab(models.Model):
    tab_name = models.CharField(max_length=200, blank=True)
    path = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=100)

    def __str__(self):
        return str(self.sort_order) + ' | ' + self.tab_name + ' | ' + self.path 

    class Meta:
        ordering = ["sort_order", "tab_name"]

class NavigationSubTab(models.Model):
    sub_tab_name = models.CharField(max_length=200, blank=True)
    parent_tab = models.ForeignKey('navigationtab', db_column='parent_tab', on_delete=models.CASCADE, null=True, blank=True)
    page = models.CharField(max_length=200, blank=True)
    path = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=100)

    def __str__(self):
        return self.sub_tab_name + ' | ' + str(self.parent_tab) + ' | ' + str(self.sort_order)

    class Meta:
        ordering = ["page", "parent_tab", "sort_order"]

class NavigationTab(models.Model):
    tab_name = models.CharField(max_length=200, blank=True)
    section = models.CharField(max_length=200, blank=True)
    page = models.CharField(max_length=200, blank=True)
    path = models.CharField(max_length=200, blank=True)
    sort_order = models.IntegerField(default=100)

    def __str__(self):
        return self.section + ' | ' + self.tab_name + ' | ' + str(self.sort_order)

    class Meta:
        ordering = ["section", "sort_order"]

