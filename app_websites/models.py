from django.db import models

class Order(models.Model):
    order_no = models.IntegerField(blank=True)
    name = models.CharField(max_length=200, blank=True) 
    address_1 = models.CharField(max_length=200, blank=True)
    address_2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_no)

    class Meta:
        ordering = ["-date"]