from django.test import TestCase
from django.urls import reverse
from .models import Item


class Buy(TestCase):

    ...
    # def test_get(self):
    #     url = reverse('payment:item', kwargs={'id': 1})
    #     response = self.client.get(url)
    #     self.assertTemplateUsed(response, 'Payment/item_detail.html')
    #     self.assertEqual(response.status_code, 200)


class ItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Item.objects.create(
            name='Test',
            price=5999,
        )

    def test_template(self):
        url = reverse('payment:item_detail', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'Payment/item_detail.html')
        self.assertEqual(response.status_code, 200)
