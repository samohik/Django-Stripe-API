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
    cart = models.CharField(verbose_name='Cart name', max_length=100, default="Test")

    def __str__(self):
        return str(self.cart)

    # def get_absolute_url(self):
    #     return reverse('payment:item', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
