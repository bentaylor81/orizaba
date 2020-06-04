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
        return str(self.order_id)

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
    billing_email = models.CharField(max_length=200, blank=True)
    billing_phone = models.CharField(max_length=200, blank=True)
    delivery_name = models.CharField(max_length=200, blank=True)
    delivery_address_1 = models.CharField(max_length=200, blank=True)
    delivery_address_2 = models.CharField(max_length=200, blank=True)
    delivery_city = models.CharField(max_length=200, blank=True)
    delivery_postcode = models.CharField(max_length=200, blank=True)
    delivery_country = models.CharField(max_length=200, blank=True)
    delivery_email = models.CharField(max_length=200, blank=True)
    delivery_phone = models.CharField(max_length=200, blank=True)
    delivery_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    ip_address = models.CharField(max_length=200, blank=True)
    website = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    month = models.CharField(max_length=3, blank=True)  
    year = models.IntegerField(blank=True) 

    def __str__(self):
        return str(self.order_no) + ' | ' + str(self.delivery_name)

    class Meta:
        ordering = ["-date"]

class Product(models.Model):
    product_id = models.IntegerField(primary_key=True)
    product_name = models.CharField(max_length=200, blank=True)	
    sku = models.CharField(max_length=200, blank=True)	
    price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)	
    weight = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=4)
    location = models.CharField(max_length=200, blank=True)	
    brand = models.ForeignKey('brand', db_column='brand', on_delete=models.CASCADE, null=True, blank=True, default='Other')
    supplier = models.ForeignKey('supplier', db_column='supplier', on_delete=models.CASCADE, null=True, blank=True, default='Unknown')
    url = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.product_id) + ' | ' + str(self.sku) + ' | ' + str(self.product_name)

    class Meta:
        ordering = ["product_id"]
        
class Supplier(models.Model):
    supplier = models.CharField(max_length=200, primary_key=True)
    path = models.CharField(max_length=200, blank=True)

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