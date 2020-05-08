from django.db import models

class Order(models.Model):
    order_no = models.IntegerField(blank=True)
    profile_pic = models.ImageField(blank=True)

    def __str__(self):
        return str(self.order_no)