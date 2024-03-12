from django.db import models
from django.utils import timezone

class Order(models.Model):
    ORDER_TYPES = (
        ('prepaid', 'Prepaid'),
        ('postpaid', 'Postpaid'),
    )
    
    merchant_id = models.IntegerField()
    order_type = models.CharField(max_length=10, choices=ORDER_TYPES)
    item_value = models.DecimalField(max_digits=10, decimal_places=2)
    taxable_value = models.DecimalField(max_digits=10, decimal_places=2)
    non_taxable_value = models.DecimalField(max_digits=10, decimal_places=2)
    loyalty_discount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_charge = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2)
    packing_charge = models.DecimalField(max_digits=10, decimal_places=2)
    total_discounted_amount = models.DecimalField(max_digits=10, decimal_places=2)
    wallet_discount = models.DecimalField(max_digits=10, decimal_places=2)
    final_bill_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_completed_date = models.DateTimeField(default=timezone.now)

    
    def __str__(self):

        return self.order_type