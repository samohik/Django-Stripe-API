from django.test import TestCase
from django.urls import reverse
from .models import Item, Tax, Discount, Order


class Base(TestCase):
    @classmethod
    def setUpTestData(cls):
        discount = Discount.objects.create()
        tax = Tax.objects.create()
        order = Order.objects.create(
            discount=discount,
            tax=tax,
        )
        Item.objects.create(
            name='Test',
            price=5999,
            order=order,
        )


class BuyViewTest(Base):
    def test_post(self):
        url = reverse('payment:buy', kwargs={'id': 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


class ItemsViewTest(Base):
    def test_get(self):
        url = reverse('payment:items')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Payment/main.html')
        self.assertEqual(response.status_code, 200)


class ItemDetailViewTest(Base):
    def test_template(self):
        url = reverse('payment:item_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Payment/item_detail.html')
        self.assertEqual(response.status_code, 200)


class OrderViewTest(Base):
    def test_get(self):
        url = reverse('payment:order', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Payment/order.html')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        url = reverse('payment:order', kwargs={'pk': 1})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
