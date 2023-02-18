from django.db import models
from django.urls import reverse


class Item(models.Model):
    name = models.CharField(verbose_name='Name', max_length=150, )
    description = models.TextField(verbose_name='Description', )
    price = models.IntegerField(verbose_name='Price in cent', default=0)
    order = models.ForeignKey('Order', related_name='items',
                              on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def price_usd(self):
        return self.price / 100

    def get_absolute_url(self):
        return reverse('payment:item', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'


class Order(models.Model):
    cart_name = models.CharField(verbose_name='Cart name', max_length=100, default="Test")
    discount = models.ForeignKey('Discount', related_name='order',
                                 on_delete=models.CASCADE, null=True, blank=True)
    tax = models.ForeignKey('Tax', related_name='order',
                            on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.cart_name)

    def items_price(self):
        res = 0
        for item in self.items.all():
            res += item.price
        return res / 100

    def get_absolute_url(self):
        return reverse('payment:order', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class Discount(models.Model):
    currency = models.CharField(verbose_name='Currency', max_length=150, default="usd",)
    percent_off = models.FloatField(verbose_name='Percent off', max_length=150, default=25,)
    duration = models.CharField(verbose_name='Duration', max_length=150, default="repeating",)
    duration_in_months = models.IntegerField(verbose_name='Duration in months', default=3,)

    def __str__(self):
        return str(self.percent_off)

    class Meta:
        verbose_name = 'Discount'
        verbose_name_plural = 'Discounts'


class Tax(models.Model):
    TAXES = [
        ('txcd_99999999', 'Tangible Goods'),
        ('txcd_10000000', 'Electronically Supplied Services'),
        ('txcd_20030000', 'Services'),
    ]
    category = models.CharField(verbose_name='Category', max_length=50,
                                choices=TAXES, default='txcd_99999999')

    def __str__(self):
        return str(self.category)

    class Meta:
        verbose_name = 'Tax'
        verbose_name_plural = 'Tax'
