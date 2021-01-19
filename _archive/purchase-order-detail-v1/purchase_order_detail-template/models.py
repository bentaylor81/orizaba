from django.db import models
import datetime

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
    comments = models.CharField(max_length=100, blank=True, null=True)
    label = models.BooleanField(default=False)
    date_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id) + ' | ' + str(self.purchaseorder.reference) + ' | ' + str(self.product.product_name) + ' | ' + str(self.order_qty) + ' | ' + str(self.received_qty) + ' | ' + str(self.outstanding_qty) + ' | ' + str(self.received_status)

    def save(self, *args, **kwargs):
        self.received_qty = (self.received_qty + self.delivery_qty) # Delivery part added to current received value
        self.delivery_qty = 0                                       # Delivery set back to 0
        self.label = False                                          # Reset the print label to False
        self.outstanding_qty = (self.order_qty - self.received_qty) # Outstanding part qty updated

        if self.outstanding_qty == 0:
            self.received_status = 'Full Receipt'
        elif self.outstanding_qty != 0 and self.outstanding_qty < self.order_qty:
            self.received_status = 'Partial Receipt'
        super(PurchaseOrderItem, self).save(*args, **kwargs) 

    class Meta:
        ordering = ["product_sku", "-id"]

class PurchaseOrder(models.Model):
    PO_CHOICES = [
        ('Pending', 'Pending'),
        ('Part Receipt', 'Part Receipt'),
        ('Unleashed', 'Unleashed'),
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