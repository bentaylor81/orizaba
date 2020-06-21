from django.db import models

class Day(models.Model):
    day = models.DateField(primary_key=True, auto_now=False, auto_now_add=False)
    item_qty = models.IntegerField(blank=True, default=0)
    order_qty = models.IntegerField(blank=True, default=0)
    item_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    delivery = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    revenue = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.day)

    class Meta:
        ordering = ["day"]

class Month(models.Model):
    month_id = models.IntegerField(primary_key=True)
    month = models.CharField(max_length=200, blank=True)
    year = models.ForeignKey('year', db_column='year', on_delete=models.CASCADE, null=True, blank=True, default=0)
    item_qty = models.IntegerField(blank=True, default=0)
    order_qty = models.IntegerField(blank=True, default=0)
    item_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    delivery = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    revenue = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.month_id) + ' | ' + str(self.month) + ' | ' + str(self.year) + ' | ' + str(self.item_qty) + ' | ' + str(self.order_qty) + ' | ' + str(self.item_price) + ' | ' + str(self.vat) + ' | ' + str(self.delivery) + ' | ' + str(self.revenue)

    class Meta:
        ordering = ["month_id"]

class Year(models.Model):
    year = models.IntegerField(primary_key=True)
    item_qty = models.IntegerField(blank=True, default=0)
    order_qty = models.IntegerField(blank=True, default=0)
    item_price = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    vat = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    delivery = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)
    revenue = models.DecimalField(blank=True, default=0, max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.year)

    class Meta:
        ordering = ["year"]
